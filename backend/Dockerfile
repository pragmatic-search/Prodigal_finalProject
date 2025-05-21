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

# --- NEW: Pre-download the HuggingFace model during build ---
# This ensures the model is part of the image, speeding up container startup.
# Requires a temporary script or direct python command.
COPY main.py . # Need main.py to run the model loading logic

# This command attempts to load the model to trigger download
# We use python -c to run a small script that tries to load the model
# and then exit. This should cache the model weights.
RUN python -c "from transformers import pipeline; import logging; logging.basicConfig(level=logging.INFO); try: pipeline('summarization', model='sshleifer/distilbart-cnn-12-6'); print('Model pre-downloaded successfully.') except Exception as e: print(f'Model pre-download failed: {e}'); raise"

# Remove main.py after pre-download to avoid copying it twice, if desired (optional)
# RUN rm main.py

# Copy the actual application code into the container (excluding initial main.py if removed above)
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]