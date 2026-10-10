const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");


// ==========================================================
// SCROLL TO BOTTOM
// ==========================================================

function scrollToBottom() {

    if (!chatBox) {
        return;
    }

    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
}


// ==========================================================
// ADD MESSAGE
// ==========================================================

function addMessage(text, sender) {

    if (!chatBox) {
        return;
    }

    const row = document.createElement("div");

    row.className =
        "message-row " + sender;

    const bubble = document.createElement("div");

    bubble.className =
        "message-bubble";

    bubble.textContent = text;

    row.appendChild(bubble);

    chatBox.appendChild(row);

    scrollToBottom();
}


// ==========================================================
// SHOW RESULTS BUTTON
// ==========================================================

function showResultsButton() {

    if (!chatBox) {
        return;
    }

    // Don't create it twice
    if (
        document.getElementById("resultsButton")
    ) {
        return;
    }

    const button =
        document.createElement("a");

    button.id =
        "resultsButton";

    button.href =
        "/results";

    button.className =
        "results-button";

    button.textContent =
        "View My Recommendations";

    chatBox.appendChild(button);

    scrollToBottom();
}


// ==========================================================
// SEND MESSAGE
// ==========================================================

let messageInProgress = false;

async function sendMessage() {

    if (messageInProgress) {
        return;
    }

    // Make sure the input exists
    if (!messageInput) {
        console.error(
            "Course Compass: message input was not found."
        );
        return;
    }

    const message =
        messageInput.value.trim();

    // Don't send empty messages
    if (!message) {
        return;
    }

    // Show user's message immediately
    addMessage(
        message,
        "user"
    );

    // Clear input
    messageInput.value = "";

    // Prevent duplicate submissions while the server is processing.
    messageInProgress = true;

    if (sendBtn) {
        sendBtn.disabled = true;
    }

    try {

        const response =
            await fetch(
                "/message",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        // Get response
        const data =
            await response.json();

        // If the server lost this chat's in-memory state (for example, after
        // a restart), start a clean chat instead of applying the answer to the
        // wrong interview question. This does not change the page's appearance.
        if (data.reset_chat) {
            window.location.href = "/start";
            return;
        }

        // --------------------------------------------------
        // SERVER ERROR
        // --------------------------------------------------

        if (!response.ok || !data.success) {

            console.error(
                "Course Compass server error:",
                data
            );

            addMessage(
                data.error ||
                "Sorry, something went wrong. Please try again.",
                "bot"
            );

            return;
        }


        // --------------------------------------------------
        // DISPLAY BOT MESSAGES
        // --------------------------------------------------

        if (Array.isArray(data.messages)) {

            data.messages.forEach(
                function(item) {

                    if (
                        item.sender === "bot"
                    ) {

                        addMessage(
                            item.text,
                            "bot"
                        );
                    }
                }
            );
        }


        // --------------------------------------------------
        // SHOW RECOMMENDATIONS BUTTON
        // --------------------------------------------------

        if (
            data.finished ||
            data.show_results
        ) {

            showResultsButton();
        }

    }

    catch (error) {

        console.error(
            "Course Compass JavaScript error:",
            error
        );

        addMessage(
            "Sorry, something went wrong while contacting Course Compass. Please try again.",
            "bot"
        );
    }

    finally {

        messageInProgress = false;

        if (sendBtn) {
            sendBtn.disabled = false;
        }

        messageInput.focus();

        scrollToBottom();
    }
}


// ==========================================================
// SEND BUTTON
// ==========================================================

if (sendBtn) {

    sendBtn.addEventListener(
        "click",
        function(event) {

            event.preventDefault();

            sendMessage();
        }
    );

} else {

    console.error(
        "Course Compass: sendBtn was not found."
    );
}


// ==========================================================
// ENTER KEY
// ==========================================================

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                event.preventDefault();

                sendMessage();
            }
        }
    );

} else {

    console.error(
        "Course Compass: message input was not found."
    );
}


// ==========================================================
// PAGE LOAD
// ==========================================================

window.addEventListener(
    "load",
    function() {

        scrollToBottom();

        if (messageInput) {
            messageInput.focus();
        }
    }
);