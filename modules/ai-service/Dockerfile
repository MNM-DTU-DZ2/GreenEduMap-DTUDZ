# AI Service Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for numpy/scipy
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app

# Run the service
CMD ["python", "-m", "app.main"]

