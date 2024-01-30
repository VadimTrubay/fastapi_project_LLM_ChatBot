# DS_Team_Project
Hello we are the best DS developers Team at GoIT DS_9 flow. 

"AI Text Analyzer" allows users to easily access advanced technologies for processing and analyzing text information 
using modern methods of artificial intelligence.

The main functionality of the project includes:

Ability to download documents in PDF, CSV, DOCX, EML, EPUB, HTML, MD, PPTX, TXT formats.
Text processing and analysis of downloaded documents using the powerful capabilities of Large Language Models (LLM).
Saving the text of documents in a vectorized database for later use.
Interact with processed documents via chat to get contextually informed answers.
Ability to create, edit and delete user profiles, save user data in the database.
Security - all users can work only with their documents.
In addition, the project provides storage of the history of requests to Large Language Models (LLM).

The additional level of functionality of the project includes the following possibilities:

Using JWT (JSON Web Tokens) for user authentication and authorization. JWT ensures the security of data transfer 
between client and server by using a signed token.

Separation of users by roles such as admin, moderator and regular user. Each role will have appropriate access 
rights to the functionality of the web service.

Email verification functionality that allows you to confirm that the specified email address belongs to the user. 
This may include sending an email with a confirmation link.

The ability to reset the user's password by email. The user can send a request to reset the password and
receive a link to change the password by e-mail.

Changing the user's avatar. Users will be able to upload their own avatars to display on their profile.

These advanced features extend the capabilities of the web service and provide a 
more convenient and secure experience for users.

Redis was also used for caching and regulating the load of requests to the server

Designing the project as a Docker image, storing it in the DockerHub repository, 
and following the step-by-step instructions for installing and using the project ensure ease of testing and deployment.


"AI Text Analyzer". This project uses technologies such as 
FastAPI, Streamlit, PostgreSQL, Docker, OpenAI, Faiss, Git, LangChain, Cloudinary, Redis.


# How to start for developers:
- update project from Git
- create environment 
```bash
poetry export --without-hashes --format requirements.txt --output requirements.txt
pip install -r requirements.txt
```
- create in root folder your own .env file like .env.example
- run docker application
- run in terminal: `docker-compose up` -> up Redis+Postgress
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run in terminal: `uvicorn main:app --host localhost --port 8000 --reload` -> start application
- run in terminal: `streamlit run PDF_Researcher.py` -> start front application
- now you have access to:
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://127.0.0.1:8000/redoc -> Redoc documentation
- http://127.0.0.1:8000/ -> template
- http://localhost:8501/ -> Streamlit frontend


# How to dokerizate the app:
- run in terminal: `docker build -t researcher .` -> create an image
- run in terminal: `docker run -p 8000:8000 -p 8501:8501 researcher` -> run your app
- run in terminal: `docker run -p 8501:8501 researcher` -> run your app


### After changes in DB models:
- `alembic revision --autogenerate -m "name"` -> generation of migration
- `alembic upgrade head` -> implementation to DB

### Shut off
- terminal with uvicorn -> Press CTRL+C to quit
- terminal with docker run: `docker-compose down` -> shut Redis+Postgres


# Good luck!!!