FROM python:3.11-trixie

WORKDIR worker

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD api/ .

#RUN ls

#CMD ["celery", "--app=tasks", "worker", "-l", "INFO"]


