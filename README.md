Moba AI is a Python portfolio project containing two AI-powered tools:

- Moba Assistant — a terminal-based writing and text helper.
- Moba AI Chatbot — a browser-based AI chatbot built with FastAPI.

Both applications use the Groq API to generate AI-powered responses. The project is organized into small, reusable files for easy development, testing, and maintenance.

Requirements

- Python 3.10+
- Groq API key
- Git (optional, for version control)

Setup (Windows / VS Code)

1. Clone or download the repository.
2. Open the "Moba-AI" folder in Visual Studio Code.
3. Open Terminal → New Terminal.
4. Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate

5. Install the required packages:

python -m pip install -r requirements.txt

6. Create your private environment file:

copy .env.example .env

7. Open ".env" and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=your_groq_model_name

Keep your actual API key private. Never upload your ".env" file to GitHub.

Run Moba Assistant

python moba_assistant.py

Choose an option to improve writing, summarize text, explain a topic, or draft a message. Enter "0" to exit.

Run Moba AI Chatbot

uvicorn app.main:app --reload

Open the following address in your browser:

"http://127.0.0.1:8000"

API documentation:

"http://127.0.0.1:8000/docs"

Run Tests

python -m pytest

Tests mock the AI service, so they do not require an API key or make actual API calls.

API Endpoints

Method| Endpoint| Description
GET| "/"| Moba chatbot interface
GET| "/health"| Health check
POST| "/api/chat"| Send a message
DELETE| "/api/chat/{conversation_id}"| Clear a conversation

Example request body:

{
  "conversation_id": "my-session",
  "message": "Explain Python functions in simple words."
}

Conversation History

Moba keeps the latest messages in server memory, separately for each conversation ID. The history is cleared when the server restarts. This is a simple demonstration and does not use persistent database storage.

Technologies Used

- Python
- FastAPI
- Groq API
- OpenAI Python SDK (Groq-compatible interface)
- HTML
- CSS
- JavaScript
- Pytest

Security and Important Notes

- Keep your ".env" file private.
- Never publish your API keys or other secrets.
- Groq API usage is subject to its current usage limits and pricing.
- Do not send sensitive personal information to this demo application.

Developer

Mohib Ullah
Computer Science Student
Creator and Developer of Moba AI
