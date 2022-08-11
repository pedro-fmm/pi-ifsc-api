FROM python:3.10

WORKDIR /api_sistema_vendas

COPY ./api_sistema_vendas /api_sistema_vendas

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]