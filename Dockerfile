FROM python:3.10-slim-buster

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#for back
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#for front
#CMD ["strimlit", "run", "./src/front_test/main_app.py"]