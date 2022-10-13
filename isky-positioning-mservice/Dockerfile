# Dockerfile
FROM python:3.9
COPY requirements.txt /positioningapp/requirements.txt
WORKDIR /positioningapp
RUN pip install -r requirements.txt
COPY . /positioningapp
ENTRYPOINT ["python"]
CMD ["run.py"]