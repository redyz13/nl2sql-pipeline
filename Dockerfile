# Use an official Python runtime as a parent image
FROM python:3.10.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire src directory into the container
COPY src /app/src

# Copy the requirements_api.txt file into the container at /app
COPY requirements_api.txt .

# Copy the data directory into the container at /app/data
COPY data /app/data

# Copy the prompts directory into the container at /app/prompts
COPY prompts/zero_shot /app/prompts/zero_shot

# Install the dependencies from requirements_api.txt
RUN pip install --no-cache-dir -r requirements_api.txt
