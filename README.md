# Flask + Keras + Gunicorn + nginx + docker

This is a small AI deployment demo with Flask + Keras + Gunicorn + nginx + docker. Please consider, the model used is for demonstration purposes (does not achieve good results yet).

Here you will find an `` app/main.py `` file that contains all the functionalities related to the IA model.

The main purpose of the system is to predict the ethnic group of the loaded image, however, the most important thing here is the deployment.

Frameworks and technologies used:

* Framework: Flask + Keras
* Servers: Gunicorn + nginx

## How to use

## Prerequisites

* Docker
* docker-compose

## Instructions

In this repository, copy the file named .env.example to .env and adjust file variables.

```
cp .env.example .env
```

Open a terminal, run the built container and build the code.

```
sudo docker-compose up --build
```

wait until installation is complete (the first time it can take a couple of minutes), then go to 
localhost in your browser to use the ethnic prediction system.

