::run this every time you update models.py

:: Creates the migrations file.
python manage.py makemigrations

:: Executes the migrations and updates the database with your model changes.
python manage.py migrate