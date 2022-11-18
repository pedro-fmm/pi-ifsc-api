FROM python:3.10-slim

WORKDIR /api_sistema_vendas

COPY ./api_sistema_vendas /api_sistema_vendas

RUN apt-get -qq update && apt-get install -y \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    libpoppler-cpp-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt \
    && pip3 install gunicorn

EXPOSE 8000

CMD gunicorn --bind [::]:8000 --workers 2 --threads 2 api_sistema_vendas.wsgi:application