FROM python:3.6.6-alpine3.7

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

EXPOSE 9000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:9000
