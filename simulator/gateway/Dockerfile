FROM python:3.12-slim
WORKDIR /app
# Install build deps for bsdiff4
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gateway_app.py .
COPY can_bus.py .
COPY templates ./templates
CMD ["python", "gateway_app.py"]
