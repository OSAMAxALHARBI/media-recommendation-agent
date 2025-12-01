import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@dataclass
class Config:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "")
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    ANILIST_API_URL: str = "https://graphql.anilist.co"
    MODEL_NAME: str = "gemini-2.0-flash-exp"

config = Config()

# Validate API keys
if not config.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Check your .env file!")
if not config.TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not found in environment variables. Check your .env file!")