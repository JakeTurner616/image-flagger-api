# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code and the .env file
COPY . .

# Initialize the database by running the init_db.py script
RUN python init_db.py

# Expose the internal port for Gunicorn
EXPOSE 5000

# Command to run the app with Gunicorn
CMD ["gunicorn", "--preload", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
