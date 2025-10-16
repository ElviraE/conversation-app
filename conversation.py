# conversation.py
import json
import os
from openai import OpenAI

client = OpenAI()
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return [{"role": "system", "content": "You are a very friendly old school teacher."}]

def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def main():
    messages = load_history()
    print("Chat started. Type /exit to quit or /clear to reset history.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"/exit", "exit", "quit"}:
            print("Goodbye!")
            save_history(messages)
            break
        elif user_input.lower() == "/reset":
            messages = [{"role": "system", "content": "You are a concise, helpful assistant."}]
            save_history(messages)
            print("History cleared.")
            continue

        messages.append({"role": "user", "content": user_input})

        # ✅ Limit history to the last 10 messages (keep conversation snappy)
        recent_messages = [messages[0]] + messages[-10:] if len(messages) > 10 else messages

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=recent_messages
        )

        reply = resp.choices[0].message.content
        print(f"Assistant: {reply}\n")

        messages.append({"role": "assistant", "content": reply})
        save_history(messages)

if __name__ == "__main__":
    main()