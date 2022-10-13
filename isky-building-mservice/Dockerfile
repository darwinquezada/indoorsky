# Dockerfile
FROM python:3.9
COPY requirements.txt /buildingapp/requirements.txt
WORKDIR /buildingapp
RUN pip install -r requirements.txt
COPY . /buildingapp
ENTRYPOINT ["python"]
CMD ["run.py"]