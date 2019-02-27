FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY development.ini /code
#COPY production.ini /code
COPY setup.cfg /code
COPY setup.py /code
RUN mkdir /code/weeehire
RUN mkdir /code/migration
COPY weeehire /code/weeehire
COPY migration /code/migration
WORKDIR /code
#RUN python3 -m venv venv
#RUN . venv/bin/activate
RUN pip install uwsgi
RUN pip install tg.devtools
RUN pip install -e .
ENV ADMIN_USERNAME 'admin'
ENV ADMIN_EMAIL 'admin@example.com'
ENV ADMIN_PASS 'ultrasecurepassword'
ENV NO_REPLY_EMAIL 'yourtestemail@example.com'
RUN gearbox setup-app
#RUN gearbox serve --reload

RUN uwsgi --paste config:/code/development.ini --socket :3031 -H /code
