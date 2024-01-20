import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

@dataclass
class Config:
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    ATHLETE_ID = os.environ.get("ATHLETE_ID")