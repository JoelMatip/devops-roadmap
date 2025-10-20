# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
CMD curl --fail http://localhost:5000/health || exit 1