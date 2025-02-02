FROM python:3.11-slim-bullseye

ENV LANGUAGE=en_US.UTF-8
ENV PGCLIENTENCODING utf8
ENV PYTHONIOENCODING utf8

ARG DOCKER_SRC=/opt/fbk_glasses_bot

# install apt requirements

COPY .docker/pkglist /tmp/pkglist
RUN set -x; apt-get update -y && apt-get install -f -y --no-install-recommends $(cat /tmp/pkglist) && apt-get clean

# install pip requirements

COPY /requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade -r /tmp/requirements.txt

# copy launch script to /

COPY .docker/launch.sh /
RUN chmod 700 /launch.sh

# copy code to source dir

RUN mkdir -p ${DOCKER_SRC}/
COPY / ${DOCKER_SRC}/

# delete the config file from docker just in case it might already contain private info

RUN rm ${DOCKER_SRC}/config.json

# finish

USER root
CMD [ "sleep", "999999" ]
