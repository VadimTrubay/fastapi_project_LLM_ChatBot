# DS_Team_Project
Hello we are the best DS developers Team at GoIT DS_9 flow. 
Long read about us.

Long read about the project.

# How to start for developers:
- update project from Git
- create environment (I use PyCharm Poetry)
```bash
poetry export --without-hashes --format requirements.txt --output requirements.txt
pip install -r requirements.txt
```
- create in root folder your own .env file like .env.example (now it's in postgres, later we'll change)
- run docker application
- run in terminal: `docker-compose up` -> up REdis+Postgress
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run in terminal: `uvicorn main:app --host localhost --port 8000 --reload` -> start application
- run in terminal: `streamlit run PDF_Researcher.py` -> start front application
- now you have access to:
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://127.0.0.1:8000/redoc -> Redoc documentation
- http://127.0.0.1:8000/ -> template


### After changes in DB models:
- `alembic revision --autogenerate -m "name"` -> generation of migration
- `alembic upgrade head` -> implementation to DB

### Shut off
- terminal with uvicorn -> Press CTRL+C to quit
- terminal with docker run: `docker-compose down` -> shut REdis+Postgress

## Already implemented functionality FastApi:
- error handler
- performance meter
- root - for template generation
- healthchecker - for check DB status
- connection limiter
- users model in DB with roles(admin, moderator, user) and profiles
- authentication JWT mechanism 
- forget password mechanism
- first version of frontend with full functionality only in streamlit, now we are going to replace functionality to backend