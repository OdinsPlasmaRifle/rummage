FROM python:3.6
ADD src/requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /app/
WORKDIR /app/
ENV HOME /app
ADD src/ /app
