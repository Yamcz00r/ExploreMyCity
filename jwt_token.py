from dotenv import load_dotenv, dotenv_values
from os import getenv
load_dotenv(dotenv_path=".env")
JWT_SECRET = getenv("JWT_SECRET")
ALGORITHM = getenv("ALGORITHM")

