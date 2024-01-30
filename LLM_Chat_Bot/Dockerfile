# Docker-команда FROM вказує базовий образ контейнера
# Use Ubuntu-based image
FROM python:3.10

# Set environment variable
ENV APP_HOME /app

# Set the working directory inside the container
WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

# Copy other files into the container's working directory
COPY . /app

# Install dependencies inside the container
RUN pip install -r requirements.txt

# Specify the port where the application runs inside the container
EXPOSE 8501

# Define environment variable
#ENV FastApi=main.py

# Run our application inside the container
CMD ["streamlit", "run", "PDF_Researcher.py"]