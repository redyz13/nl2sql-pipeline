# Use an official Python runtime as a parent image
FROM python:3.10.11-slim

# Install PostgreSQL dependencies and gcc for psycopg2 compilation
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy the entire src directory into the container
COPY src /app/src

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app
