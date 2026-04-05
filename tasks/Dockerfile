FROM python:3.11-trixie

RUN pip install celery

ADD celery.py tasks.py

CMD python tasks.py