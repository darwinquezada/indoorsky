# Dockerfile
FROM python:3.9
COPY requirements.txt /cleansingapp/requirements.txt
WORKDIR /cleansingapp
RUN pip install -r requirements.txt
COPY . /cleansingapp
ENTRYPOINT ["python"]
CMD ["run.py"]