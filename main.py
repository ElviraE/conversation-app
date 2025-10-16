import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for the AI
system_prompt = """You are running an animal guessing game. Follow these rules:
1. Pick one random animal at the very start and remember it throughout the entire game
2. Ask the player what category to choose from (mammals, birds, reptiles)
3. Give the player a descriptive clue about this animal without saying its name
4. The player has exactly 5 attempts to guess the animal
5. Keep track of how many attempts the player has used
6. If they guess correctly, say "Congrats! The animal was [animal name]"
7. If they guess wrong, say "Try again!" and give them a short,friendly helpful hint after 3 wrong guesses
8. After 5 wrong guesses, say "Not today, the animal was [animal name]"
9. Never change the animal mid-game
10. Add dificukty levels (easy/medium/hard descriptions)
11. Add scoring system based on attempts used 
12. Be super friendly!"""

# Start conversation with system prompt
messages = [{"role": "system", "content": system_prompt}]

print("Welcome to my Animal Guessing Game!")
print("=" * 50)
print("Commands: /reset (new game) | /exit (quit game)")
print()

# Ask AI to start the game
messages.append({"role": "user", "content": "Start the game and give me the first clue!"})

# Get the initial clue
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True
)

# Display clue character by character
ai_response = ""
for chunk in stream:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
        ai_response += content

print("\n")

# Add AI's response to conversation history
messages.append({"role": "assistant", "content": ai_response})

# Main game loop
while True:
    # Get user's guess
    user_guess = input("Your guess: ").strip()
    
    # Skip empty inputs
    if not user_guess:
        print("Please enter a guess!")
        continue
    
    # Check for /exit command
    if user_guess.lower() == "/exit":
        print("\nExiting game. See you next time!")
        break
    
    # Check for /reset command
    if user_guess.lower() == "/reset":
        print("\nResetting game...\n")
        # Clear conversation history but keep system prompt
        messages = [{"role": "system", "content": system_prompt}]
        # Start new game
        messages.append({"role": "user", "content": "Start the game and give me the first clue!"})
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        
        ai_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                ai_response += content
        
        print("\n")
        messages.append({"role": "assistant", "content": ai_response})
        continue
    
    # Add guess to conversation
    messages.append({"role": "user", "content": user_guess})
    
    # Get AI's response to the guess
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )
    
    # Display response character by character
    ai_response = ""
    print("\nAI: ", end="", flush=True)
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            ai_response += content
    
    print("\n")
    
    # Add AI's response to conversation history
    messages.append({"role": "assistant", "content": ai_response})
    
    # Check if game ended (won or lost)
    if "congratulations" in ai_response.lower() or "not today" in ai_response.lower():
        print("Thanks, it was fun!")
        break