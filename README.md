
# Book Management API

This project is a Book Management API built with FastAPI. It allows you to manage books, add reviews, and get book recommendations based on user preferences.

## Important Note!!!
I attempted to obtain an SSL certificate from Certbot, but Amazon Linux 2 did not support it. After trying unsuccessfully to obtain a different SSL certificate, I created a self-signed certificate using Diffie-Hellman Parameters. Since I am using this self-signed SSL certificate with Nginx, a warning will appear when accessing the public DNS, but this is acceptable for testing purposes. For a more secure SSL certificate, I could use certbot-nginx, but this would require purchasing or owning a domain name, which I am not able to do at the moment.<br><br>

## Features

- Add, update, delete, and retrieve books
- Add and retrieve reviews for books
- Get book recommendations based on genres, authors, and keywords
- Generate summaries for books
- Continuous Integration and Deployment with GitHub Actions

## Installation

### Prerequisites

- AWS account with an EC2 instance running Amazon Linux 2
- PostgreSQL database
- Python 3.7+
- Nginx
- Uvicorn
- Certbot (optional for HTTPS with Let's Encrypt)

### Clone the repository
git clone https://github.com/callmeblaze/book_management.git<br>
cd book_management

### Set up the virtual environment and install dependencies
python -m venv venv<br>
source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`<br>
pip install -r requirements.txt<br>
Configure the database<br>
Set up a PostgreSQL database on AWS RDS.<br>
Create a config.py file in the root directory with the following content:

### Configure Nginx

Create a new Nginx configuration file:

    sudo nano /etc/nginx/conf.d/fastapi.conf

Add the following configuration:<br>

Create Diffie-Hellman Parameters(Not Recommended for Production):

    sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
    
nginx

    server {
    listen 80;
    server_name ec2-13-53-168-255.eu-north-1.compute.amazonaws.com;

    location / {
        return 301 https://$host$request_uri;
    }
    }

    server {
    listen 443 ssl;
    server_name ec2-13-53-168-255.eu-north-1.compute.amazonaws.com;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Security headers
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
        add_header X-Content-Type-Options nosniff;
        add_header X-Frame-Options DENY;
        add_header X-XSS-Protection "1; mode=block";
        add_header Referrer-Policy same-origin;
        add_header Permissions-Policy "geolocation=(self)";
    }
    }


Restart Nginx

    sudo systemctl restart nginx

Check Nginx Status

    sudo systemctl status nginx

stop Nginx 

    sudo systemctl stop nginx

Start Uvicorn
Run Uvicorn in the background:

    nohup uvicorn main:app --host 0.0.0.0 --port 8000 &

Check Uvicorn Status:

    ps aux | grep uvicorn

Check Logs for Errors

    sudo tail -f /var/log/nginx/error.log
    sudo tail -f /var/log/nginx/access.log

#### Access the Application
Try accessing your application using both HTTP and HTTPS:

HTTP: http://ec2-13-53-168-255.eu-north-1.compute.amazonaws.com<br>
HTTPS: https://ec2-13-53-168-255.eu-north-1.compute.amazonaws.com<br>

### Run the application
uvicorn main:app --host 0.0.0.0 --port 8000

### swagger UI browser
http://ec2-13-53-168-255.eu-north-1.compute.amazonaws.com:8000/docs

### API Endpoints
#### Books:
POST /books: Add a new book<br>
GET /books: Retrieve all books<br>
GET /books/{id}: Retrieve a specific book by its ID<br>
PUT /books/{id}: Update a book's information by its ID<br>
DELETE /books/{id}: Delete a book by its ID

#### Reviews:
POST /books/{id}/reviews: Add a review for a book<br>
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
FastAPI: https://fastapi.tiangolo.com/<br>
SQLAlchemy: https://www.sqlalchemy.org/<br>
Ollama: https://ollama.com/<br>
GitHub Actions: https://github.com/features/actions
