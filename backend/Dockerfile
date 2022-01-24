# pull official base image
FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /usr/src/app
# install dependencies
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy our django project
COPY pet_project .

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
