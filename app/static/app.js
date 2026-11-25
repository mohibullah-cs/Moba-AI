const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const welcome = document.querySelector("#welcome");
const sendButton = document.querySelector("#send-button");
const newChatButton = document.querySelector("#new-chat");

let conversationId = createConversationId();

function createConversationId() {
    if (window.crypto && window.crypto.randomUUID) {
        return window.crypto.randomUUID();
    }
    return `chat-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function addMessage(role, text) {
    welcome.hidden = true;

    const row = document.createElement("div");
    row.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "Y" : "M";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    // textContent keeps model output as text instead of rendering HTML.
    bubble.textContent = text;

    row.append(avatar, bubble);
    messages.appendChild(row);
    row.scrollIntoView({ behavior: "smooth", block: "end" });
    return row;
}

async function sendMessage(message) {
    addMessage("user", message);
    input.value = "";
    input.style.height = "auto";
    sendButton.disabled = true;

    const loadingRow = addMessage("assistant", "Moba is thinking...");
    loadingRow.querySelector(".bubble").classList.add("typing");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                conversation_id: conversationId,
                message
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong. Please try again.");
        }
        loadingRow.querySelector(".bubble").textContent = data.reply;
        loadingRow.querySelector(".bubble").classList.remove("typing");
    } catch (error) {
        loadingRow.querySelector(".bubble").textContent = error.message;
        loadingRow.querySelector(".bubble").classList.remove("typing");
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (message && !sendButton.disabled) {
        sendMessage(message);
    }
});

input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
});

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
    }
});

document.querySelectorAll(".suggestion").forEach((button) => {
    button.addEventListener("click", () => sendMessage(button.textContent));
});

newChatButton.addEventListener("click", async () => {
    try {
        await fetch(`/api/chat/${encodeURIComponent(conversationId)}`, {
            method: "DELETE"
        });
    } catch (_) {
        // Starting a fresh local conversation still works if clearing fails.
    }
    conversationId = createConversationId();
    messages.replaceChildren();
    welcome.hidden = false;
    input.focus();
});
