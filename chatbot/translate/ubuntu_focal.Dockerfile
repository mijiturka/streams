FROM ubuntu:focal
WORKDIR /translateLocally
COPY translateLocally-Ubuntu-20.04.deb .

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
  apt-get -y upgrade

RUN apt-get -y install \
  libpcre++-dev \

  libarchive-dev \
  libarchive13 \

  libprotobuf-dev \

  qttools5-dev \
  qtbase5-dev \
  libqt5svg5-dev \
  qttools5-dev-tools \
  libqt5core5a \
  libqt5gui5 \
  libqt5network5 \
  libqt5svg5 \
  libqt5widgets5 \

  libc6 \
  libstdc++6 \

  libgcc-s1

RUN dpkg -i translateLocally-Ubuntu-20.04.deb

RUN translateLocally -v

RUN translateLocally -d bg-en-tiny
RUN translateLocally -d cs-en-base
RUN translateLocally -d cs-en-tiny
RUN translateLocally -d de-en-base
RUN translateLocally -d de-en-tiny
RUN translateLocally -d es-en-tiny
RUN translateLocally -d et-en-tiny
RUN translateLocally -d fr-en-tiny
RUN translateLocally -d is-en-tiny
RUN translateLocally -d nb-en-tiny
RUN translateLocally -d nn-en-tiny
RUN translateLocally -d pl-en-tiny

RUN apt-get -y install python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY lid.176.ftz .

COPY identify.py .
COPY text_to_translate.md .

RUN cat text_to_translate.md | translateLocally -m $(python3 identify.py)-en-tiny

CMD tail -f /dev/null
