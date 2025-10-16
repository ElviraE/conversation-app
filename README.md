1. Setup Instructions

Step 1: Install required packages

bash  pip install openai python-dotenv

Step 2: Get OpenAI API key (with link)
Step 3: Set up environment variables (.env file)


2. How to Play

Command to run the game: python3 main.py
Game rules (5 attempts, AI gives clues)
Special commands (/reset and /exit)

Key Features

The AI (GPT-3.5-turbo) handles:

Selecting a random animal (from three categories: mammals, birds, reptiles)
Generating clues
Tracking the number of attempts
Validating guesses
Determining when the game ends


Streaming Responses: Text appears character-by-character for a better user experience
Conversation History: The game maintains context through the entire conversation, allowing the AI to remember what animal it picked and how many attempts have been made
No Python State Tracking: All game logic is handled by the AI through prompts and conversation context, not Python variables

Security Note:

- Never commit your `.env` file to version control
- The `.gitignore` file ensures `.env` is excluded from Git
- Only share `.env.example` (which has no real API key)
- Keep your API key private at all times


animal-guessing-game/
├── main.py          ✅ Game code with /exit and /reset
├── .env             ✅ Your secret API key
├── .env.example     ✅ Template
├── .gitignore       ✅ Protects your .env
└── README.md        ✅ Complete documentation


