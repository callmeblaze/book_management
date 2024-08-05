import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import config
from models import Book, Review

DATABASE_URL = f"postgresql://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}/{config.DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

query = """
SELECT books.id, books.title, books.genre, AVG(reviews.rating) as avg_rating
FROM books
JOIN reviews ON books.id = reviews.book_id
GROUP BY books.id
"""

with engine.connect() as connection:
    result = connection.execute(text(query))
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

session.close()

df['genre'] = df['genre'].astype('category').cat.codes

X = df[['genre', 'avg_rating']]
y = df['avg_rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, 'book_recommendation_model.pkl')

print("Model training complete and saved as book_recommendation_model.pkl")
