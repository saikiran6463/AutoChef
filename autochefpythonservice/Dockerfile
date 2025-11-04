# Use Python 3.11 slim image as base
# 'slim' variant is smaller and more secure than full Python image
FROM python:3.11-slim

# Set working directory inside container
# All subsequent commands will run from this directory
WORKDIR /app

# Copy requirements first (before app code)
# This optimizes Docker layer caching - if code changes but requirements don't,
# Docker can reuse the layer with installed dependencies
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir saves space by not storing pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# This comes after pip install to optimize caching
COPY app/ ./app/

# Expose port 8000 where FastAPI will run
# This is documentation - doesn't actually publish the port
EXPOSE 8000

# Command to run the application
# uvicorn runs the FastAPI app on all interfaces (0.0.0.0) port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]