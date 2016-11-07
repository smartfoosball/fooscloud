FROM ax003d/docker-python:latest

MAINTAINER Robert Zheng <rzheng@xtremeprog.com>

RUN mkdir -p /app
WORKDIR /app
RUN pip install -r deploy/requirements.txt
ADD . /app
ADD nginx.conf /etc/nginx/nginx.conf
ADD app.conf /etc/nginx/sites-available/app
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
RUN rm -f /etc/nginx/sites-enabled/default
RUN mkdir -p /data/nginx
RUN mkdir -p /data/supervisor

VOLUME /data/nginx
VOLUME /data/supervisor
EXPOSE 80

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-n", "-c", "supervisord.conf.docker"]