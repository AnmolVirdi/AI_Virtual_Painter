FROM ubuntu:latest

MAINTAINER AnmolVirdi

RUN apt update &&\
    apt install python3.7.9 &&\
    apt-get install python3-opencv &&\
    pip3 install numpy &&\
    pip3 install mediapipe &&\
    pip3 install os &&\
    pip3 install opencv-python &&\
    mkdir /AI_Virtual_Painter

COPY . /AI_Virtual_Painter

WORKDIR /AI_Virtual_Painter

ENTRYPOINT python3 main.py


