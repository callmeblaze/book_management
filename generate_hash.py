from passlib.context import CryptContext
import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

password = config.PASSWORD
hashed_password = hash_password(password)
print(f"Hashed password: {hashed_password}")
