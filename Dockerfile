# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent .pyc files and enable stdout/stderr logging
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt  requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Install Redis
RUN apt-get update && apt-get install -y redis-server && rm -rf /var/lib/apt/lists/*

# Run Redis as a background service
RUN service redis-server start

# Set up Celery and Redis broker URL
ENV CELERY_BROKER_URL=redis://redis:6379/0

# Expose port 8000 for Django and 6379 for Redis
EXPOSE 8000 6379

# # Start Redis, Django, and Celery
# CMD ["bash", "-c", "service redis-server start && celery -A your_project_name worker -l info & celery -A your_project_name beat -l info & python manage.py runserver 0.0.0.0:8000"]
