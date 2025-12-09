from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
