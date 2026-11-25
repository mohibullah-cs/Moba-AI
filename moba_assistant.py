"""Command-line Moba Assistant for everyday text tasks."""

from app.ai_service import AIServiceError, get_ai_reply

TASKS = {
    "1": (
        "Improve the grammar, clarity, and flow of the following text. "
        "Keep the original meaning and return only the improved version."
    ),
    "2": (
        "Summarize the following text in clear, simple language. "
        "Use a short paragraph and bullets when useful."
    ),
    "3": (
        "Explain the following topic to a beginner using simple language "
        "and one practical example."
    ),
    "4": (
        "Draft a natural, polite message based on the user's notes. "
        "Do not invent names, dates, or facts."
    ),
}


def get_user_choice() -> str:
    print("\n--- Moba Assistant ---")
    print("1. Improve my writing")
    print("2. Summarize text")
    print("3. Explain a topic")
    print("4. Draft a message")
    print("0. Exit")
    return input("\nChoose an option: ").strip()


def run_assistant() -> None:
    print("Welcome to Moba Assistant.")

    while True:
        choice = get_user_choice()

        if choice == "0":
            print("Thanks for using Moba Assistant. Goodbye!")
            break

        instruction = TASKS.get(choice)
        if instruction is None:
            print("Please choose a number from 0 to 4.")
            continue

        user_text = input("\nEnter your text or topic: ").strip()
        if not user_text:
            print("Please enter some text first.")
            continue

        messages = [
           {
    "role": "system",
    "content": (
        "You are Moba AI, an AI assistant created and developed "
        "by Mohib Ullah. Your creator is Mohib Ullah "
        "or Groq. Groq provides the API infrastructure used to "
        "power your responses. If someone asks who created you, "
        "credit Mohib Ullah."
    )
}
        ]

        try:
            result = get_ai_reply(messages)
            print("\nMoba Assistant:")
            print(result)
        except AIServiceError as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    run_assistant()
