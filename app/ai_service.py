"""Groq AI service for Moba AI.
Developed by Mohib Ullah.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIServiceError(Exception):
    """Raised when the AI service cannot return a response."""


# Moba AI identity and creator information
MOBA_IDENTITY = """
You are Moba AI, an intelligent AI assistant application.

YOUR CREATOR:
Your application was created and developed by Mohib Ullah.

IDENTITY RULES:
1. Your name is Moba AI.
2. Mohib Ullah is your creator and developer.
3. When asked who created you, always credit Mohib Ullah.
4. When asked who developed Moba AI, answer Mohib Ullah.
7. Be honest about your underlying technology.

TECHNOLOGY:
Moba AI is an independent AI assistant application
developed by Mohib Ullah.
It uses Groq API infrastructure and the configured
underlying language model to generate responses.

CREATOR RESPONSE:
If someone asks who created you, respond:

"I am Moba AI, an AI assistant created and developed
by Mohib Ullah."

Always maintain this identity throughout the conversation.
"""


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Create and reuse the Groq API client."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise AIServiceError(
            "Moba AI configuration error: API credentials are missing."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        timeout=30.0,
        max_retries=2,
    )


def get_ai_reply(messages: list[dict[str, str]]) -> str:
    """Generate an AI response using Groq."""

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    try:
        # Preserve the original conversation
        conversation = [
            dict(message) for message in messages
        ]

        # Add Moba's identity to the system instructions
        system_message = next(
            (
                message for message in conversation
                if message.get("role") == "system"
            ),
            None
        )

        if system_message:
            system_message["content"] = (
                str(system_message.get("content", ""))
                + "\n\n"
                + MOBA_IDENTITY
            )
        else:
            conversation.insert(
                0,
                {
                    "role": "system",
                    "content": MOBA_IDENTITY
                }
            )

        # Request response from Groq
        response = get_client().chat.completions.create(
            model=model,
            messages=conversation,
            temperature=0.5,
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():
            raise AIServiceError(
                "Moba AI could not generate a response. Please try again."
            )

        return answer.strip()

    except AIServiceError:
        raise

    except Exception as exc:
        # Keep technical details out of the user-facing response
        raise AIServiceError(
            "Moba AI is temporarily unavailable. "
            "Please check your connection and try again."
        ) from exc