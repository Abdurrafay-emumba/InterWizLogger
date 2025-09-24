# Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# If you don't want a separate requirements.txt, you can install Flask directly
RUN pip install --no-cache-dir Flask

# Copy only your app (keeps image smaller)
COPY app.py /app/

# Create the logs directory in the container
RUN mkdir -p /app/logs

EXPOSE 4598

CMD ["python", "app.py"]
