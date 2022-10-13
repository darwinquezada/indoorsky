# Dockerfile
FROM python:3.9
COPY requirements.txt /floorapp/requirements.txt
WORKDIR /floorapp
RUN pip install -r requirements.txt
COPY . /floorapp
ENTRYPOINT ["python"]
CMD ["run.py"]