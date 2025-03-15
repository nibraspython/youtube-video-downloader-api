# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Run the app using Gunicorn (Flask needs WSGI, not ASGI)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
