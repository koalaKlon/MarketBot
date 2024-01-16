FROM python:3.11.3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/djangoapp/src

WORKDIR /opt/services/djangoapp/src

COPY requirements.txt /opt/services/djangoapp/src/requirements.txt
RUN pip install -r requirements.txt

COPY . /opt/services/djangoapp/src

EXPOSE 80

CMD ["python", "main.py"]