# ee1037-grouph
## Requirements

* Python 3.9+
* Visual Studio Code  
  * Extension: "Python" (ms-python.python)
* Docker (optional, for Docker setup)

## Local Development

### Instructions

To run the project locally:

1. Open the project in Visual Studio Code.
2. Set up a virtual environment:
   - Press `F1` -> "Python: Create Environment" -> Select "Venv" -> Choose `requirements.txt`.
3. Select the Python interpreter:
   - Press `F1` -> "Python: Select Interpreter" -> Choose the `.venv` environment.
4. Run the following commands in the terminal:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # Use credentials like admin/admin for initial setup
   python manage.py runserver  # Host defaults to localhost
   * Open <http://localhost:8000> in the web browser.
   Note: Ensure your database settings in mysite/settings.py use localhost as the host.
   

To run the project using Docker:

1.Clean up previous Docker artifacts
    docker-compose down --volumes --remove-orphans

2. Build and start the containers:

    docker-compose up --build

This will apply database migrations and create a superuser with username 'admin' and password 'admin123'

The application will be available at http://localhost:8000.

Note: In Docker, the database host is configured as db in mysite/settings.py. Ensure your Docker setup reflects this.