import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for the AI
system_prompt = """You are an expert Animal Game Host with 10 years of experience...
Your personality: enthusiastic, encouraging, and knowledgeable about animals. All animal descriptions must be accurate and biologically correct. Follow these rules:
1. Pick one random animal at the very start and remember it throughout the entire game
2. Ask the player what category to choose from (mammals, birds, reptiles)
3. Give the player a descriptive clue about this animal without saying its name
4. The player has exactly 5 attempts to guess the animal
5. Keep track of how many attempts the player has used
6. If they guess correctly, say "Congrats! The animal was [animal name]"
7. If they guess wrong, say "Try again!" and give them a short,friendly helpful hint after 3 wrong guesses
8. After 5 wrong guesses, say "Not today, the animal was [animal name]"
9. Never change the animal mid-game
10. Add difficulty levels (easy/medium/hard descriptions)
11. Add scoring system based on attempts used 
12. Be super friendly!"""

# FEW-SHOT PROMPTING
# Few-shot prompting provides examples to guide the AI's behavior

few_shot_examples = """
EXAMPLE INTERACTIONS (Few-Shot Learning):

Example 1 - Starting the game:
User: "Start the game"
You: "Welcome! Choose a category: mammals, birds, or reptiles?"

Example 2 - After category selection:
User: "mammals"
You: "Great choice! I'm thinking of a mammal that lives in Africa, has a long trunk, and is the largest land animal. What's your guess? (Attempt 1/5)"

Example 3 - Wrong guess:
User: "rhino"
You: "Not quite! Try again. Hint: This animal is known for its excellent memory. (Attempt 2/5)"

Example 4 - Correct guess:
User: "elephant"
You: "Congrats! The animal was an elephant! 🎉 You guessed it in 3 attempts. Great job!"

Example 5 - Game over (all attempts used):
User: "lion" (5th wrong guess)
You: "Not today! The animal was an elephant. Thanks for playing! Want to try again?"

Now, follow these examples when running the actual game.
"""

# Combine system prompt with few-shot examples
full_system_prompt = system_prompt + "\n\n" + few_shot_examples

# TEMPERATURE

# Temperature controls randomness/creativity (0.0 = deterministic, 1.0 = balanced, 2.0 = very random)
# - Low temperature (0.0-0.3): Focused, consistent, predictable responses
# - Medium temperature (0.4-0.7): Balanced creativity and consistency
# - High temperature (0.8-1.0): Creative, varied responses

TEMPERATURE_SETTINGS = {
    "easy": 0.3,      # Low creativity - straightforward clues
    "medium": 0.7,    # Balanced - moderately creative clues
    "hard": 0.9       # High creativity - creative, tricky clues (within 0-1 range)
}

# MAX_TOKENS

# Max tokens limits the response length
# 1 token ≈ 4 characters or 0.75 words
# Setting limits prevents overly long responses

MAX_TOKENS_SETTINGS = {
    "easy": 150,      # Longer, more detailed clues
    "medium": 100,    # Moderate length clues
    "hard": 80        # Shorter, concise clues (harder to guess)
}

# TOP_P

# Top_p controls diversity by considering only top probability tokens
# - Low top_p (0.1-0.5): More focused, less diverse
# - High top_p (0.9-1.0): More diverse, varied vocabulary

TOP_P_SETTINGS = {
    "easy": 0.5,      # Focused vocabulary
    "medium": 0.8,    # Balanced diversity
    "hard": 0.95      # Highly diverse vocabulary
}


# GAME SETUP

# Start conversation with system prompt
messages = [{"role": "system", "content": full_system_prompt}]

print("Welcome to my Animal Guessing Game!")
print("=" * 50)
print("Commands: /reset (new game) | /exit (quit game)")
print()
print("\n🎯 Choose difficulty level:")
print("  1. Easy   - Simple clues, more details")
print("  2. Medium - Balanced challenge")
print("  3. Hard   - Tricky clues, less details")

while True:
    difficulty_choice = input("\nEnter 1, 2, or 3: ").strip()
    if difficulty_choice == "1":
        difficulty = "easy"
        break
    elif difficulty_choice == "2":
        difficulty = "medium"
        break
    elif difficulty_choice == "3":
        difficulty = "hard"
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

# Set parameters based on difficulty
current_temperature = TEMPERATURE_SETTINGS[difficulty]
current_max_tokens = MAX_TOKENS_SETTINGS[difficulty]
current_top_p = TOP_P_SETTINGS[difficulty]

# Ask AI to start the game
messages.append({"role": "user", "content": "Start the game and give me the first clue!"})

# Get the initial clue
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=current_temperature,    # Controls creativity
    max_tokens=current_max_tokens,      # Limits response length
    top_p=current_top_p,                # Controls diversity
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
        messages = [{"role": "system", "content": full_system_prompt}]
        
        # Ask for new difficulty
        print("🎯 Choose new difficulty:")
        print("  1. Easy   2. Medium   3. Hard")
        
        while True:
            difficulty_choice = input("Enter 1, 2, or 3: ").strip()
            if difficulty_choice in ["1", "2", "3"]:
                difficulty = ["easy", "medium", "hard"][int(difficulty_choice) - 1]
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        # Update parameters
        current_temperature = TEMPERATURE_SETTINGS[difficulty]
        current_max_tokens = MAX_TOKENS_SETTINGS[difficulty]
        current_top_p = TOP_P_SETTINGS[difficulty]
        
        # Start new game
        messages.append({"role": "user", "content": "Start the game and give me the first clue!"})
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=current_temperature,
            max_tokens=current_max_tokens,
            top_p=current_top_p,
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
        temperature=current_temperature,    # Creativity level
        max_tokens=current_max_tokens,      # Response length limit
        top_p=current_top_p,                # Vocabulary diversity
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
