**Setting up a new environment**

python3 -m venv env
source env/bin/activate


**Requirements**

open requirements.txt file to see requirements

To install requirements type
pip install -r requirements.txt

**Installing**

open terminal and type
git clone the repo or simply download using the url 

**To migrate the database open terminal in project directory and type**

python manage.py makemigrations
python manage.py migrate

Creating Superuser

To create superuser open terminal and type
python manage.py createsuperuser

To run the program in local server use the following command

python manage.py runserver

Then go to http://127.0.0.1:8000 in your browser to see available endpoints
