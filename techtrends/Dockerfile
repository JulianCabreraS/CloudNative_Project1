FROM python:3.8
LABEL maintainer="Julian Cabrera"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "init_db.py" ]
CMD [ "python", "app.py" ]
EXPOSE 3111/tcp
