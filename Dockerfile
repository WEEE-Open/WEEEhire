FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code && mkdir /code/weeehire && mkdir /code/migration
WORKDIR /code
COPY setup.cfg /code
COPY setup.py /code
COPY migration /code/migration
COPY weeehire /code/weeehire
COPY production.ini.example /code
COPY production.ini.example /code/development.ini
RUN pip install tg.devtools uwsgi
RUN pip install -e .
ENV ADMIN_USERNAME 'admin'
ENV ADMIN_EMAIL 'admin@example.com'
ENV ADMIN_PASS 'ultrasecurepassword'
ENV NO_REPLY_EMAIL 'yourtestemail@example.com'
RUN gearbox setup-app
#RUN gearbox serve --reload
CMD ["uwsgi", "--paste", "config:/code/development.ini", "--socket", ":3031", "-H", "/code"]
