FROM python:3.7-slim

RUN groupadd user && useradd -ms /bin/bash -g user user

RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && \
    apt-get install -qq -y binutils build-essential mime-support gettext iproute2 libproj-dev gdal-bin && \
    pip install -q --no-cache-dir -U pip && \
    pip install -q --no-cache-dir uwsgi && \
    pip install -q --no-cache-dir pipenv

COPY . /home/user/code

WORKDIR /home/user/code

RUN pipenv lock -r >/home/user/requirements.txt && \
    pip install -q --no-cache-dir -r /home/user/requirements.txt

COPY ./docker/uwsgi.ini /etc/uwsgi.ini
COPY ./docker/build-staticfiles.sh ./docker/start.sh /

RUN chmod +x /build-staticfiles.sh
RUN chmod +x /start.sh

EXPOSE 5050

ENTRYPOINT ["/start.sh"]

CMD ["uwsgi", "--ini", "/etc/uwsgi.ini"]
