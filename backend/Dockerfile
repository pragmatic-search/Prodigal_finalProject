# Use a lightweight Python base image
FROM python:3.10-slim-buster

# Set environment variable for HuggingFace cache directory (optional, but good practice)
ENV HF_HOME=/app/.cache/huggingface

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application code into the container
# This copies everything from your local 'backend' directory into '/app' in the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
# --host 0.0.0.0 makes the server accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]