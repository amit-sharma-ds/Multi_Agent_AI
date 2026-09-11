from dotenv import load_dotenv

from agno.db.sqlite import SqliteDb

load_dotenv(override=True)

db = SqliteDb(
    db_file="agent_memory.db"
)