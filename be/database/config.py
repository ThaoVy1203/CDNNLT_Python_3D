import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    SERVER = os.getenv("DB_SERVER", "localhost")
    DATABASE = os.getenv("DB_NAME", "dbCDNNLT")
    USERNAME = os.getenv("DB_USER", "sa")
    PASSWORD = os.getenv("DB_PASSWORD", "123456")
