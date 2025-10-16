# conversation.py
from openai import OpenAI
import os

def main():
    client = OpenAI()  # reads OPENAI_API_KEY from env by default

    system_prompt = "You are a concise, helpful assistant."
    messages = [{"role": "system", "content": system_prompt}]

    print("Chat started. Type /reset to clear, /exit to quit.")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        # Commands
        if user_input.lower() in {"/exit", "exit", "quit"}:
            print("Goodbye!")
            break
        if user_input.lower() == "/reset":
            messages = [{"role": "system", "content": system_prompt}]
            print("(history cleared)")
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"(error) {e}"

        print(f"Assistant: {reply}\n")
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
