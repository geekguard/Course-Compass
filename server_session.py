"""SQLite-backed server-side sessions for Course Compass.

Only a random session ID is stored in the browser cookie. The session contents,
including the conversation transcript and chatbot state, remain on the server.
This avoids putting the full chat transcript into Flask's client-side cookie and
allows the application to restore a student's interview after a process restart.
"""

from __future__ import annotations

import json
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from typing import Any

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict


class SQLiteSession(CallbackDict, SessionMixin):
    """A small dictionary-like Flask session backed by SQLite."""

    def __init__(self, initial: dict[str, Any] | None = None, sid: str | None = None, new: bool = False):
        def on_update(_session: "SQLiteSession") -> None:
            _session.modified = True

        super().__init__(initial or {}, on_update)
        self.sid = sid or secrets.token_urlsafe(32)
        self.new = new
        self.modified = False


class SQLiteSessionInterface(SessionInterface):
    """Store Flask sessions in a local SQLite database."""

    session_class = SQLiteSession

    def __init__(self, database_path: str, lifetime_seconds: int = 7 * 24 * 60 * 60):
        self.database_path = database_path
        self.lifetime_seconds = lifetime_seconds
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        self._initialize_database()

    @contextmanager
    def _connection(self):
        connection = sqlite3.connect(self.database_path, timeout=10)
        try:
            connection.execute("PRAGMA journal_mode=WAL")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize_database(self) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS server_sessions (
                    sid TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    expires_at REAL NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_server_sessions_expiry "
                "ON server_sessions(expires_at)"
            )

    def open_session(self, app, request):
        cookie_name = self.get_cookie_name(app)
        sid = request.cookies.get(cookie_name)

        if sid:
            now = time.time()
            try:
                with self._connection() as connection:
                    row = connection.execute(
                        "SELECT data, expires_at FROM server_sessions WHERE sid = ?",
                        (sid,),
                    ).fetchone()

                    if row and row[1] > now:
                        data = json.loads(row[0])
                        if isinstance(data, dict):
                            return self.session_class(data, sid=sid)

                    if row:
                        connection.execute(
                            "DELETE FROM server_sessions WHERE sid = ?", (sid,)
                        )
            except (sqlite3.Error, json.JSONDecodeError, TypeError, ValueError):
                app.logger.exception("Could not load the saved Course Compass session")

        return self.session_class({}, sid=secrets.token_urlsafe(32), new=True)

    def save_session(self, app, session, response) -> None:
        cookie_name = self.get_cookie_name(app)
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if not session:
            try:
                with self._connection() as connection:
                    connection.execute(
                        "DELETE FROM server_sessions WHERE sid = ?", (session.sid,)
                    )
            except sqlite3.Error:
                app.logger.exception("Could not clear the saved Course Compass session")

            if session.modified:
                response.delete_cookie(
                    cookie_name,
                    domain=domain,
                    path=path,
                    secure=self.get_cookie_secure(app),
                    httponly=self.get_cookie_httponly(app),
                    samesite=self.get_cookie_samesite(app),
                )
            return

        expires_at = time.time() + self.lifetime_seconds
        try:
            encoded = json.dumps(dict(session), ensure_ascii=False, separators=(",", ":"))
            with self._connection() as connection:
                connection.execute(
                    """
                    INSERT INTO server_sessions (sid, data, expires_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(sid) DO UPDATE SET
                        data = excluded.data,
                        expires_at = excluded.expires_at
                    """,
                    (session.sid, encoded, expires_at),
                )
                # Expired sessions are removed as part of normal traffic.
                connection.execute(
                    "DELETE FROM server_sessions WHERE expires_at <= ?", (time.time(),)
                )
        except (sqlite3.Error, TypeError, ValueError):
            app.logger.exception("Could not save the Course Compass session")
            raise

        response.set_cookie(
            cookie_name,
            session.sid,
            expires=self.get_expiration_time(app, session),
            httponly=self.get_cookie_httponly(app),
            secure=self.get_cookie_secure(app),
            samesite=self.get_cookie_samesite(app),
            path=path,
            domain=domain,
        )
