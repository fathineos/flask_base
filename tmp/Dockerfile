FROM debian:latest

RUN apt-get update -qq &&\
    apt-get install -qq -y --force-yes build-essential apt-utils git netcat &&\
    apt-get clean

RUN ["/bin/bash"]
