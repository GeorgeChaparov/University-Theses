# University-Theses

## 1. About the project
This project use Docker and Docker Conteiner to create self-hosted jupyter lab.
If you don't want to run the self-hosted jupyter, you can check the final python code inside the src folder.

## 2. How to run Jupyter Lab

> [!IMPORTANT]
> You need to have Docker installed.

To build the image navigate to "Docker" folder and run this command: `docker build -t fastai-jupyter-lab:latest .`
The build might take more then 10 min for all dipendences to be downloaded and the image to be created. 

While in the same folder compose up the docker compose file using: "docker compose up"

In the console you should see something like `fastai-jupyter-lab  |         http://127.0.0.1:8888/lab token=9e2fc2582cef6685a32e932fe7102dbb5ae258c95ef103ab`. Copy and paste the link in a browzer of your choise.