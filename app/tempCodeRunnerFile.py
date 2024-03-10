from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

