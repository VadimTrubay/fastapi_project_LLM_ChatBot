# LLM_ChatBot
Welcome to Team 6. We have created a convenient personal chatbot for work that reads and recognizes documents. 
It's like a cool assistant that gets everything you need from your files and answers your questions with context and more.

"LLM_ChatBot" allows users to easily access advanced technologies for processing and analyzing text information 
using modern methods of artificial intelligence.

The main functionality of the project includes:

It is possible to download data and convert it into text from an Internet link or from a link to a YouTube video, 
as well as documents in PDF, DOCX, TXT formats.
It is also possible to get answers to any questions by talking with GPT-3.5.

Text processing and analysis of downloaded documents using the powerful capabilities of Large Language Models (LLM).
Saving the text of documents in a vectorized database for later use.
Interact with processed documents via chat to get contextually informed answers.
Ability to create user profiles, save user data in the database.
Security - all users can work only with their documents.
In addition, the project provides storage of the history of requests to Large Language Models (LLM).

The additional level of functionality of the project includes the following possibilities:

Using JWT (JSON Web Tokens) for user authentication and authorization. JWT ensures the security of data transfer 
between client and server by using a signed token.

Email verification functionality that allows you to confirm that the specified email address belongs to the user. 
This may include sending an email with a confirmation link.

The ability to reset the user's password by email. The user can send a request to reset the password and
receive a link to change the password by e-mail.

"LLM_ChatBot". This project uses technologies such as 
FastAPI, Streamlit, PostgresSQL, Docker, OpenAI, Faiss, Git, LangChain, Cloudinary, Redis.


# How to start for developers:
- update project from Git
- create environment 
- pip install -r requirements.txt
- create in root folder your own .env file like .env.example
- run docker application

- run in terminal: `docker-compose up` -> up Redis + Postgres
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run in terminal: `uvicorn main:app --host localhost --port 8000 --reload` -> start application
- run in terminal: `streamlit run main_app.py` -> start front application

- now you have access to:
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://localhost:8501/ -> Streamlit frontend

# Shut off
- terminal with uvicorn -> Press CTRL+C to quit
- terminal with docker run: `docker-compose down` -> shut Redis+Postgres


