# Classifier API

API to extract classification from a text/image classifier trained and validated offline. Created using FastAPI

## Project Structure
```
classifier_api
│   main.py # code defining API configs and entrypoint
│   model_selection.py # code for running either image or text model
│   router.py # code for API get request
│   config.py
│   errors.py
│
└── models # large model files saved here, ideally should be in a storage container
```

## Pre-requisites
* [Docker](https://www.docker.com/products/docker-desktop)

## Pre-requisites for development
* [Uvicorn](https://pypi.org/project/uvicorn/)
* [Poetry](https://python-poetry.org/docs/)
* [Pre-commit](https://pre-commit.com)

## Quick Start

1. Create and run docker image
```
docker build -t classifier_api .
docker run -d --name api_container -p 80:80 classifier_api
```
2. Query API
```
import requests

payload = {'name': 'Print Dress', 'description': 'Dress', 'product_id':128544}
response = requests.get('http://0.0.0.0:80/api/v1/predict', params=payload)
response.json()
```
3. Interact with Fast API docs
    - http://0.0.0.0:80/docs
    - http://0.0.0.0:80/redoc

## Installation

1. Run poetry
```
cd classifier.api
poetry install
```
2. Run API locally
```
uvicorn classifier_api:main:app --reload
```
