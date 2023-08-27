ARG CARLA_VERSION
FROM carlasim/carla:0.9.13 AS carla_api

FROM python:3.8.16-slim-bullseye
# FROM pytorch/pytorch
ARG CARLA_VERSION

#Install Python Carla API
COPY --from=carla_api --chown=root /home/carla/PythonAPI/carla /opt/carla/PythonAPI
WORKDIR /opt/carla/PythonAPI

RUN pip3 install carla==0.9.13
RUN pip3 install jupyter
RUN pip3 install torch torchvision torchaudio
RUN pip3 install matplotlib

COPY --chown=root carla_data_collector.py /root/carla_client/
COPY --chown=root carla_dataset.py /root/carla_client/
WORKDIR /root/carla_client
