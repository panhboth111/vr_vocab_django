# vr_vocab_django
This is an web APIs which is use as a backend of the project that allows developers to visualize data being transfered through the API and return response and handles the process of the project such as Sign Up, Sign In and (retrieve, read, write, update,etc.) the data from the postgresql database as a CRUD operations.
## Technology
* django REST framework
* Python
* Postgresql
## Django REST Framework
Is a powerful and flexible toolkit for building Web APIs.
## Virtual Environment (venv)
Virtual environment is the tool in python which help us in creating new virtual environments for our project, with their own directories, isolated from the system directories.
## Installation
Use the package manager pip to install Virtualenv
```bash
pip install virtualenv
```
Build virtual environment for the local directory
```bash
python -m venv "venv_name"
```
Activate virtual environment
### Ubuntu
```bash
source venv_name/bins/activate
```
### Window
```bash
venv_name\Scripts\activate
```
Install the requirements.txt which is contains all the packages
```bash
pip install -r requirements.txt
```
## Setup and Install Postgresql
To setup and install postgresql please follow the bellow reference
* [Setup and Install Postgresql](https://www.postgresqltutorial.com/install-postgresql/)
## Connect django to Posgresql
Go to **settings.py** and fill the bellow database connections
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'database_password',
        'HOST': 'IP address/Localhost',
        'PORT': '5432',
    }
}
```
## Start a Django Project
Migrations
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
Run Server
```bash
python manage.py runserver
```
## Get Involed!
We are happy and ready to recieve the feedback, fixes, bugs and other improvements.
PLease leave your comment for the bugs reporting.
