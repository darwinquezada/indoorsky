# Dockerfile
FROM python:3.9
COPY requirements.txt /wifiapp/requirements.txt
WORKDIR /wifiapp
RUN pip install -r requirements.txt
COPY . /wifiapp
ENTRYPOINT ["python"]
CMD ["run.py"]