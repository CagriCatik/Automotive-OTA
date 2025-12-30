FROM python:3.10-slim

WORKDIR /var/www/html

# We will mount the artifacts volume here, or copy them.
# For now, just serve the directory.

CMD ["python", "-m", "http.server", "8082"]
