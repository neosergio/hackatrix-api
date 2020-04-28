# myeventsbx
Events API

# How to run in vscode
* Install the desired python release: https://www.python.org/downloads/release/python-376/
* Install Python extension in vscode, developer is Microsoft
* Ctrl + Shift + P -> Pythong: Select Interpreter and select the correct version (for this project is 3.7.6)
* Open new terminal
* Run: "python --version or python3 --version" and verify the correct version i shown
* Run: "python -m venv .venv" (this creates a virtual environment, it allows to install dependencies in it instead of the global environment)
* Run: "pip install pipenv" (this allows to sync dependencies from Pipfile)

# First run
* Set the following environment variable in the virtual environment: "DJANGO_SETTINGS_MODULE=MyEvents.settings.local"
* Run migrations through the following commands:
	* python manage.py makemigrations
	* python manage.py migrate
	* python manage.py loaddata <fixture-name>.json (fixture-name corresponds to json files located in the users folder)

# Running
* Run the program: python manage.py runserver