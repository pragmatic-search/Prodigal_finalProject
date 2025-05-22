FROM python:3.9-slim

WORKDIR /app

# Install CPU-only PyTorch first
RUN pip install --no-cache-dir torch==2.2.2 --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY ./backend /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]