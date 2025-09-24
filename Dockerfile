# Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only your app (keeps image smaller)
COPY app.py /app/

# Create the logs directory in the container
RUN mkdir -p /app/logs

EXPOSE 4598

CMD ["python", "app.py"]
