FROM python:3.12-slim

COPY requirements.txt .

# Increase timeout and add retries
RUN pip install --no-cache-dir --default-timeout=100 --retries=10 -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
