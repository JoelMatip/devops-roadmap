# Use the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python file into the container
COPY app.py .

# Run the Python script
CMD ["python", "app.py"]