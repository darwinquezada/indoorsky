# Dockerfile
FROM python:3.9
COPY requirements.txt /preprocessingapp/requirements.txt
WORKDIR /preprocessingapp
RUN pip install -r requirements.txt
COPY . /preprocessingapp
ENTRYPOINT ["python"]
CMD ["run.py"]