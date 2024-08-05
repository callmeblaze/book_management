from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import joblib
import pandas as pd
import config
import requests
from models import Book as BookModel, Review as ReviewModel
from schemas import Book, BookCreate, BookUpdate, Review, ReviewCreate, SummaryResponse, Recommendation, UserPreferences
from typing import List
from sqlalchemy import text
import logging
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()

DATABASE_URL = f"postgresql+asyncpg://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}/{config.DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

LLAMA3_API_URL = "http://localhost:11434/api/generate"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_summary(text):
    payload = {
        "model": "llama3",
        "prompt": text,
        "stream": False,
        "options": {
            "num_predict": 50
        }
    }
    response = requests.post(LLAMA3_API_URL, json=payload)
    if response.status_code == 200:
        logger.debug(f"Response from Llama3: {response.json()}")
        return response.json().get("response", "")
    else:
        logger.error(f"Error from Llama3 API: {response.status_code} - {response.text}")
        return None

model = joblib.load('book_recommendation_model.pkl')

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    username = config.BASIC_AUTH_USERNAME
    password_hash = config.BASIC_AUTH_PASSWORD_HASH
    if credentials.username == username and pwd_context.verify(credentials.password, password_hash):
        return credentials.username
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )

@app.post("/books", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    new_book = BookModel(**book.dict())
    new_book.summary = generate_summary(book.title + " " + book.author + " " + book.genre)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@app.get("/books", response_model=List[Book])
async def get_books(db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    result = await db.execute(select(BookModel))
    books = result.scalars().all()
    return books

@app.get("/books/{id}", response_model=Book)
async def get_book(id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    book_result = await db.execute(select(BookModel).filter(BookModel.id == id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{id}", response_model=Book)
async def update_book(id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    book_result = await db.execute(select(BookModel).filter(BookModel.id == id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book

@app.delete("/books/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    book_result = await db.execute(select(BookModel).filter(BookModel.id == id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}

@app.post("/books/{id}/reviews", response_model=Review)
async def create_review(id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    book_result = await db.execute(select(BookModel).filter(BookModel.id == id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    review_data = review.dict(exclude={"book_id"})
    new_review = ReviewModel(**review_data, book_id=id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@app.get("/books/{id}/reviews", response_model=List[Review])
async def get_reviews(id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    result = await db.execute(select(ReviewModel).filter(ReviewModel.book_id == id))
    reviews = result.scalars().all()
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found")
    return reviews

@app.get("/books/{id}/summary", response_model=SummaryResponse)
async def get_summary(id: int, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    book_result = await db.execute(select(BookModel).filter(BookModel.id == id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    result = await db.execute(select(ReviewModel).filter(ReviewModel.book_id == id))
    reviews = result.scalars().all()
    rating = sum([review.rating for review in reviews]) / len(reviews) if reviews else None
    return SummaryResponse(summary=book.summary, rating=rating)

@app.post("/generate-summary", response_model=SummaryResponse)
async def generate_summary_endpoint(text: str, username: str = Depends(get_current_username)):
    summary = generate_summary(text)
    if not summary:
        raise HTTPException(status_code=500, detail="Failed to generate summary")
    return {"summary": summary}

@app.post("/recommendations", response_model=List[Recommendation])
async def get_recommendations(preferences: UserPreferences, db: AsyncSession = Depends(get_db), username: str = Depends(get_current_username)):
    query = text("""
    SELECT books.id, books.title, books.author, books.genre, AVG(reviews.rating) as avg_rating
    FROM books
    JOIN reviews ON books.id = reviews.book_id
    GROUP BY books.id
    """)
    result = await db.execute(query)
    books = result.fetchall()

    genre_map = {genre: idx for idx, genre in
                 enumerate(set(book[3] for book in books))}
    X_new = []
    for genre in preferences.genres:
        for rating in range(1, 6):
            X_new.append([genre_map[genre], rating])

    predicted_ratings = model.predict(X_new)

    recommendations_df = pd.DataFrame(X_new, columns=['genre', 'rating'])
    recommendations_df['predicted_rating'] = predicted_ratings

    recommendations_df['genre'] = recommendations_df['genre'].map({v: k for k, v in genre_map.items()})
    recommendations = []
    for genre in preferences.genres:
        for _, row in recommendations_df[recommendations_df['genre'] == genre].sort_values(by='predicted_rating',
                                                                                           ascending=False).iterrows():
            for book in books:
                if book[3] == genre and round(book[4]) == row['rating']:
                    recommendations.append({"title": book[1], "author": book[2]})
                    if len(recommendations) >= 10:
                        break
            if len(recommendations) >= 10:
                break
        if len(recommendations) >= 10:
            break

    return recommendations

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
