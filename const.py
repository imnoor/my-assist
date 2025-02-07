import os
from dotenv import load_dotenv
CHAT_HISTORY_DB = "chat_history.db"
CHAT_HISTORY_FILE = "chat_history.json"
SESSION_FILE = "chat_sessions.json"
DEFAULT_MESSAGE = {
    "Default": [{"role": "system", "content": "You are a helpful assistant."}]
}

# Default model and available models
DEFAULT_MODEL = "deepseek-r1:latest"
AVAILABLE_MODELS = [
    "deepseek-r1:latest",
    "deepseek-v3",
    "deepseek-coder"
]
