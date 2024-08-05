
# Book Management API

This project is a Book Management API built with FastAPI. It allows you to manage books, add reviews, and get book recommendations based on user preferences.

## Features

- Add, update, delete, and retrieve books
- Add and retrieve reviews for books
- Get book recommendations based on genres, authors, and keywords
- Generate summaries for books
- Continuous Integration and Deployment with GitHub Actions

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- AWS account

### Clone the repository
git clone https://github.com/callmeblaze/book_management.git
cd book_management

### Set up the virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
pip install -r requirements.txt
Configure the database
Set up a PostgreSQL database on AWS RDS.
Create a config.py file in the root directory with the following content:

### Run the application
uvicorn main:app --host 0.0.0.0 --port 8000

### swagger UI browser
http://ec2-13-53-168-255.eu-north-1.compute.amazonaws.com:8000/docs

### API Endpoints
#### Books:
POST /books: Add a new book
GET /books: Retrieve all books
GET /books/{id}: Retrieve a specific book by its ID
PUT /books/{id}: Update a book's information by its ID
DELETE /books/{id}: Delete a book by its ID

#### Reviews:
POST /books/{id}/reviews: Add a review for a book
GET /books/{id}/reviews: Retrieve all reviews for a book

#### Recommendations:
POST /recommendations: Get book recommendations based on user preferences

#### Summary:
GET /books/{id}/summary: Get a summary and aggregated rating for a book
POST /generate-summary: Generate a summary for a given book content

#### Machine Learning Model:
The project includes a machine learning model to recommend books based on genre and average rating. The model is trained on a sample dataset of books.

Model Used
We used the Random Forest Regressor model from the scikit-learn library for the recommendation system.
To train the model, run the train_model.py script:
python train_model.py


### Deployment
The project is deployed to an AWS EC2 instance. GitHub Actions is used for Continuous Integration and Deployment.

GitHub Actions Workflow
code branch: master
A GitHub Actions workflow (deploy.yml) is set up to automate the deployment process. The workflow performs the following steps:

Check out the code
Set up Python
Install dependencies
Copy files to the EC2 instance
SSH into the EC2 instance and restart the FastAPI service


### Acknowledgments
FastAPI: https://fastapi.tiangolo.com/
SQLAlchemy: https://www.sqlalchemy.org/
Ollama: https://ollama.com/
GitHub Actions: https://github.com/features/actions
