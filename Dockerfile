FROM python:3.4
ADD . /code
WORKDIR /code
CMD ["python", "app.py"]

