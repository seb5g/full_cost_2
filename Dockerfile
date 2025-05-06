# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/fullcost

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
apt-get --yes install build-essential python3-dev libmemcached-dev libldap2-dev libsasl2-dev libzbar-dev  ldap-utils tox lcov valgrind netcat && \
apt-get clean

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY . .

RUN pip install -e .

# copy entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/fullcost/entrypoint.sh
RUN chmod +x /usr/src/fullcost/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/fullcost/entrypoint.sh"]


