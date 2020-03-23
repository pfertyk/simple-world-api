# World API

A simple REST API with world data (countries, cities, languages). A web application
for accessing data easily is included.

The program uses [this database](https://ftp.postgresql.org/pub/projects/pgFoundry/dbsamples/world/world-1.0/world-1.0.tar.gz). The original file was not altered and is included in the repo.

## Installation

### Database

Install docker and docker-compose.  Navigate to the main directory and run:

```
docker-compose up
```

### REST API

The API used Django REST Framework. Installation on a Ubuntu-based system:

```
sudo apt install libpg-dev
cd backend_django
pip install -r requirement.txt
python manage.py runserver
```

Then the API can be accessed in a web browser under `localhost:8000/api`.

### Web application

The web application used React. Before installing make sure that `BASE_API_URL`
in `frontend_react/src/api.js` is set to your machine's IP address, otherwise
you will not be able to access the API from a different computer/smartphone.

To install the application follow these instructions:

```
cd frontend_react
npm install
npm start
```

Then you can access the application in your browser: `localhost:3000`.

### Tests

Django tests are provided:

```
python manage.py test world_api
```
