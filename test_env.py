# test_env.py (robust .env loader)
from dotenv import load_dotenv
from pathlib import Path
import os

here = Path(__file__).resolve().parent
dotenv_path = here / ".env"
print("Expecting .env at:", dotenv_path)

loaded = load_dotenv(dotenv_path=str(dotenv_path))
print("load_dotenv returned:", loaded)

# show raw file preview (first 200 chars) without showing full key
try:
    raw = dotenv_path.read_text(encoding='utf-8', errors='replace')
    print("first 60 chars of .env file:", raw[:60].replace("\n","\\n"))
except Exception as e:
    print("Could not read .env file directly:", e)

key = os.getenv("YOUTUBE_API_KEY")
print("YOUTUBE_API_KEY =", key)

