FROM python:3.9

USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN mkdir -p /work

# RUN apt-get update && apt-get install -y \
#     texlive-fonts-recommended \
#     && rm -rf /var/lib/apt/lists/*

ARG UNAME=pyuser
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash -d /config $UNAME

RUN mkdir /build
COPY . /build
COPY docker-entrypoint.sh /

RUN chmod 775 /docker-entrypoint.sh &&\
    chown -R $UNAME:$UNAME /build &&\
    chown -R $UNAME:$UNAME /config &&\
    chmod -R 775 /config

WORKDIR /build

USER $UNAME
ENV PATH=$PATH:/config/.local/bin

RUN pip install . --user &\
    pip install -r requirements.txt --user

WORKDIR /home/${UNAME}

ENTRYPOINT ["/docker-entrypoint.sh"]

