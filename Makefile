make test:
	python manage.py test

server:
	python manage.py runserver

coverage:
	coverage run --source='.' manage.py test
	coverage html --omit=laboratory/asgi.py,laboratory/wsgi.py,manage.py,*/management/*
	coverage report --omit=laboratory/asgi.py,laboratory/wsgi.py,manage.py,*/management/* --fail-under=100

migrate:
	python manage.py migrate

pylint:
	pylint $(shell git ls-files '*.py')

lint:
	make pylint
