admin:
	python3 manage.py createsuperuser --username admin --email admin@gmail.com


mig:
	python3 manage.py makemigrations
	python3 manage.py migrate


install-req:
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

freeze-req:
	pip3 freeze > requirements.txt


run:
	python3 manage.py runserver 0.0.0.0:8000

