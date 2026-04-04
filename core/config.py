from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set. Add it to your .env file.")

if not ALGORITHM:
    raise RuntimeError("ALGORITHM is not set. Add it to your .env file.")

if not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES is not set. Add it to your .env file.")