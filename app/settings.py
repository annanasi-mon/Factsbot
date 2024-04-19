from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MESSAGE_HISTORY_DB_DIR = 'sqlite:///' + os.path.join(BASE_DIR, 'message_history_db/message_history_db.db')

MODEL_NAME = "gpt-3.5-turbo"