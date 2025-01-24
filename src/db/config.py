import os

POSTGRES_DB = os.environ.get("POSTGRES_DB", "t2i-attacks")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "animcogn")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS", "wnx8nfg5ekeHFH35ymx")

POSTGRES_DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}/{POSTGRES_DB}"
