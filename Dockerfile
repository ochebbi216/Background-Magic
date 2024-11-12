# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories for uploads and outputs
RUN mkdir /app/uploads /app/outputs

# Expose port 5000 for Flask
EXPOSE 5000

# Set environment variable for Flask app
ENV FLASK_APP=app.py

# Run Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
