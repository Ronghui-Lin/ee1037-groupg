# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application code into the container
COPY . .

# Expose the port the app runs on (default 8000 for Django)
EXPOSE 8000

# Run Django development server (use production server in production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




# Copy your SQL script into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432
