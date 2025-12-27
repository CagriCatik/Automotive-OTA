FROM python:3.12-slim
WORKDIR /app
# Install build deps for bsdiff4/cryptography
RUN apt-get update && apt-get install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY orchestrator.py .
CMD ["python", "orchestrator.py"]
