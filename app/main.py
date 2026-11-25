"""FastAPI application for the Moba chatbot."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.ai_service import AIServiceError, get_ai_reply
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="Moba",
    description="A simple AI chatbot with conversation history.",
    version="1.0.0",
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are Moba, a helpful and friendly AI assistant. "
        "Give clear, useful answers. If a question is unclear, ask a short "
        "follow-up question. Do not claim to have done things you cannot do.\n\n"

        "DEVELOPER INFORMATION:\n"
        "Your developer and creator is Mohib Ullah.\n"
        "He was born on 15 September 2005.\n"
        "He is 21 years old as of November 2026.\n"
        "He is a CS student.\n"
        "His name in Urdu is محب اللہ.\n"
        "When writing his name in Urdu, always use exactly محب اللہ.\n"
        "Never write his name as موہیب or محیب.\n\n"

        "If someone asks who Mohib Ullah is, introduce him as "
        "the developer and creator of Moba AI. Share the information "
        "provided above when relevant. Do not invent personal details."
    ),
}

# Demo storage: conversation history is kept until the server stops.
conversations: dict[str, list[dict[str, str]]] = {}
MAX_HISTORY_MESSAGES = 20


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Moba"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation = conversations.setdefault(
        request.conversation_id, [SYSTEM_MESSAGE.copy()]
    )
    conversation.append({"role": "user", "content": request.message})

    # Keep the system message plus the most recent conversation messages.
    conversation[:] = [conversation[0]] + conversation[1:][-MAX_HISTORY_MESSAGES:]

    try:
        reply = get_ai_reply(conversation)
    except AIServiceError as exc:
        # Do not leave a failed user message in the saved history.
        conversation.pop()
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    conversation.append({"role": "assistant", "content": reply})
    return ChatResponse(conversation_id=request.conversation_id, reply=reply)


@app.delete("/api/chat/{conversation_id}")
def clear_chat(conversation_id: str):
    conversations.pop(conversation_id, None)
    return {"message": "Conversation cleared."}
