# pyrefly: ignore [missing-import]
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set in .env")

if not MONGODB_DATABASE:
    raise ValueError("MONGODB_DATABASE is not set in .env")

client = MongoClient(MONGODB_URL)

db = client[MONGODB_DATABASE]