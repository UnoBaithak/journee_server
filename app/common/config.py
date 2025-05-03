import os
from dotenv import load_dotenv
load_dotenv("app_config.env")

class Config:
    FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")