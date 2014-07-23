FROM ubuntu:12.04
MAINTAINER Proton "feisuzhu@163.com"

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install nginx-extras
RUN apt-get -y install curl wget
RUN apt-get -y install python2.7 supervisor
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python
RUN easy_install pip
RUN pip install zc.buildout

ADD nginx.conf /etc/nginx/nginx.conf
ADD apps.conf /etc/supervisor/conf.d/apps.conf
ADD cors.conf /upload/cors.conf

ADD upload_processor /upload/upload_processor
WORKDIR /upload/upload_processor
RUN buildout -vv

RUN mkdir -p /upload/files
RUN chown -R www-data:www-data /upload/files

ADD upload.json /upload/upload.json

EXPOSE 80

CMD /upload/upload_processor/bin/ensure_dirs; exec supervisord -n
