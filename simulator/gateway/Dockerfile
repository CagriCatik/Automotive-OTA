FROM python:3.12-slim
WORKDIR /app
# Install build deps for bsdiff4
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
COPY templates ./templates
COPY static ./static
COPY ota.proto .
COPY trace_logger.py .

# Build protos
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ota.proto

CMD ["python", "gateway_app.py"]
