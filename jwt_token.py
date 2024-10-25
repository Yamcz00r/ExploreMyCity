from dotenv import load_dotenv, dotenv_values
from os import getenv

load_dotenv(dotenv_path=".env")
JWT_SECRET = getenv("JWT_SECRET")
ALGORITHM = getenv("ALGORITHM")
OPEN_WEATHER_API_KEY = getenv("OPEN_APIKEY")
