FROM python:3.6.2

RUN code_name=$(cat /etc/os-release | grep "VERSION=" | sed 's/\([0-9]\|.*(\|)\"\|VERSION=\)//g') && \
    echo "deb http://mirrors.aliyun.com/debian/ $code_name main non-free contrib" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ $code_name main non-free contrib" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y \
	nginx  \
	supervisor &&\
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

COPY pip.conf requirements.txt /app/

RUN cp /app/pip.conf /etc/pip.conf -f && \
    pip install uwsgi==2.0.15 && \
    pip install -r /app/requirements.txt --upgrade-strategy only-if-needed && \
    rm -rf ~/.cache/pip

COPY . /app/

RUN cp /app/nginx.conf /etc/nginx/nginx.conf -f && \
    cp /app/supervisor-app.conf /etc/supervisor/conf.d/ && \
    mkdir /var/log/uwsgi/ && touch /var/log/uwsgi/uwsgi_evalapi_bee.log


EXPOSE 80

CMD ["supervisord", "-n"]