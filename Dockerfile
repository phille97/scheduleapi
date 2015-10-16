##
## Schedule API
## Made by Philip Johansson
## Repo: https://github.com/phille97/scheduleapi-server
##

FROM ubuntu

MAINTAINER Philip Johansson (https://github.com/phille97)

RUN apt-get update
RUN apt-get -y install git python python-setuptools nodejs npm

# Clone the git repo
git clone https://github.com/phille97/scheduleapi.git /opt/scheduleapi
cd /opt/scheduleapi

# Install the app
python setup.py install
npm install
grunt

# TODO: Setup database and run it. (Supervisord or something...)
