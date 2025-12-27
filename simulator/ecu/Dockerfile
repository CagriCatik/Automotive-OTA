FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ecu_app.py .
COPY can_bus.py .
CMD ["python", "ecu_app.py"]
