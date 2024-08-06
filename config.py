from dotenv import load_dotenv
import os

load_dotenv("local.env")

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD_HASH = os.getenv("BASIC_AUTH_PASSWORD_HASH")
PASSWORD = os.getenv("PASSWORD")
