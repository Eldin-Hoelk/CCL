# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run the Flask application
CMD ["gunicorn", "-w", "2", "--threads", "4", "-b", "0.0.0.0:5000", "app:app"]