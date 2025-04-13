# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set environment variable for Django settings module (matches manage.py)
ENV DJANGO_SETTINGS_MODULE=mysite.settings

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# - netcat: for the entrypoint wait script
# - postgresql-client: for database CLI tools (like psql, pg_isready)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the Python dependencies
# Ensure requirements.txt includes: django, psycopg2-binary, python-decouple, gunicorn (optional)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script to run on container start
# It will handle setup before running the CMD
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run the application (passed to entrypoint.sh)
# Use runserver for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
