FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1
ENV APP_HOME /app
WORKDIR /back/



COPY . /back/
RUN pip install --no-cache-dir -r /back/requirements.txt
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
