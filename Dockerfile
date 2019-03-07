# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu1604py36:latest

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	git \
	nginx \
	supervisor \
	sqlite3 


RUN apt-get install -y python-mysqldb
RUN apt-get install -y libmysqlclient-dev

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi
RUN pip3 install mysqlclient
#RUN pip3 install MySQL-python


# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
WORKDIR /home/docker/code/

COPY app/requirements.txt app/
RUN pip3 install -r app/requirements.txt

# add (the rest of) our code
COPY . .

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
# RUN django-admin.py startproject website /home/docker/code/app/

ENV DJANGO_SETTINGS_MODULE=fantasy_hockey.prod_settings
ENV STATIC_ROOT=/home/docker/code/app/static
#RUN django-admin collectstatic
# RUN cd /home/docker/code/app && python3.6 manage.py collectstatic  --noinput


EXPOSE 80
CMD ./docker-entrypoint.sh
