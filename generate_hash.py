from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

password = "gogreen"
hashed_password = hash_password(password)
print(f"Hashed password: {hashed_password}")
