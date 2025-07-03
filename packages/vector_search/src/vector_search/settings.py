import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    print(f"Loaded settings: OPENAI_API_KEY={OPENAI_API_KEY}")
