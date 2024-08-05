from pydantic import BaseModel
from typing import Optional, List

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    summary: str
    rating: Optional[float] = None

class Recommendation(BaseModel):
    title: str
    author: str

class UserPreferences(BaseModel):
    genres: List[str]
    authors: List[str]
    keywords: List[str]
