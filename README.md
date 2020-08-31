# Face segmentation demo

This is a small AI deployment demo with Flask.

Here you will find an `` app/main.py `` file that contains all the functionalities related to the IA model.

The main purpose of the system is to segment the faces of the uploaded photo.

## How to use

## Prerequisites

* Docker
* docker-compose

## Instructions
Deployment. <br>
In this repository, copy the file named .env.example to .env and adjust file variables.

```
cp .env.example .env
```

Open a terminal, run the built container and build the code.

```
sudo docker-compose up --build
```

wait until installation is complete (the first time it can take a couple of minutes), then go to localhost:9000 in your browser.

Debug mode (python 3.6 >= strongly recommended).

```
cd app
conda env create -f environment.yml
conda activate keras_gunicorn_nginx_flask
python main.py
```