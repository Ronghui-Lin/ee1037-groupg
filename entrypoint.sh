#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Variables from Environment (passed via docker-compose) ---
# Superuser details (use defaults if not set, but should be set in .env)
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-changeme} # SET THIS IN .env!

# Database connection details (needed for the wait check)
DB_HOST=${SQL_HOST:-db} # Use 'db' as default service name
DB_PORT=${SQL_PORT:-5432} # Default PG port

# --- Wait for Database ---
echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
# Loop until the host and port are available
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Database unavailable, sleeping for 1 second..."
  sleep 1acme/management/commands/commands/__init__.py acme/management/commands/commands/seed_machines.py
done
echo "Database available!"

# --- Django Setup Commands ---

# Apply database migrations
# Uses DJANGO_SETTINGS_MODULE already set in the environment (Dockerfile/compose)
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Checking for superuser '$SUPERUSER_USERNAME'..."
# Use Django shell to check existence, exit code 0=exists, 1=does not exist
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(username='$SUPERUSER_USERNAME').exists() else exit(1)"; then
    echo "Superuser '$SUPERUSER_USERNAME' already exists. Skipping creation."
else
    echo "Creating superuser '$SUPERUSER_USERNAME'..."
    # Pass credentials via environment variables expected by createsuperuser --noinput
    export DJANGO_SUPERUSER_USERNAME=$SUPERUSER_USERNAME
    export DJANGO_SUPERUSER_EMAIL=$SUPERUSER_EMAIL
    export DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD

    python manage.py createsuperuser --noinput || echo "Superuser creation failed (check logs for details)."
    # Unset password variable after use (optional security measure)
    unset DJANGO_SUPERUSER_PASSWORD
fi

# Seed initial machine data using our custom management command
echo "Running command to seed initial 'acme' machine data (if needed)..."
python manage.py seed_machines # The command itself should check if data exists

# Optional: Collect static files (Uncomment if needed for your deployment)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput --clear

# --- Start Application ---
# Execute the command passed as CMD in Dockerfile (e.g., gunicorn or runserver)
echo "Setup complete. Starting application server..."
exec "$@"