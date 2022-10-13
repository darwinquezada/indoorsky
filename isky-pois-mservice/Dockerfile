# Dockerfile
FROM python:3.9
COPY requirements.txt /poiapp/requirements.txt
WORKDIR /poiapp
RUN pip install -r requirements.txt
COPY . /poiapp
ENTRYPOINT ["python"]
CMD ["run.py"]