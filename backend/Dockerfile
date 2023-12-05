FROM docker.repos.balad.ir/python:3.12-rc-bullseye

VOLUME /prometheus_multiproc_dir

RUN apt update; apt install -y libicu-dev netcat gettext && apt upgrade --only-upgrade ca-certificates tzdata -y

ADD requirements.txt /root/requirements.txt
RUN pip install --no-cache-dir -r /root/requirements.txt

ADD . /app
WORKDIR /app/

ENTRYPOINT ["bash", "docker-entrypoint.sh"]