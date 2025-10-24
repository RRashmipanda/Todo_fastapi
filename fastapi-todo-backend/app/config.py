from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("db_name", "todo_db")
