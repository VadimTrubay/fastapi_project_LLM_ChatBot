# Project "AI Text Analyzer"

"AI Text Analyzer" allows users to easily access advanced technologies for processing and analyzing text information 
using modern methods of artificial intelligence.

The main functionality of the project includes:

Ability to download documents in PDF, CSV, DOCX, HTML, TXT formats.
Text processing and analysis of downloaded documents using the powerful capabilities of Large Language Models (LLM).
Saving the text of documents in a vectorized database for later use.
Interact with processed documents via chat to get contextually informed answers.
Ability to create, edit and delete user profiles, save user data in the database.
Security - all users can work only with their documents.
In addition, the project provides storage of the history of requests to Large Language Models (LLM).


# How to start for developers:
- update project from Git repository https://github.com/VadimTrubay/fastapi_project_LLM_ChatBot.git
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
