FROM python:3.9

USER root

RUN mkdir /work

ARG UNAME=thelper
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash -d /config $UNAME

RUN mkdir /build
COPY . /build

COPY ./docker-entrypoint.sh /
RUN chmod 775 /docker-entrypoint.sh


WORKDIR /build
RUN pip install --upgrade pip &\
    pip install . &\
    pip install -r requirements.txt

WORKDIR /work

RUN rm -rf /build

USER $UNAME

ENTRYPOINT ["/docker-entrypoint.sh"]
