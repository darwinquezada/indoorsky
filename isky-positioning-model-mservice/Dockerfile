# Dockerfile
FROM python:3.9
COPY requirements.txt /posmodelapp/requirements.txt
WORKDIR /posmodelapp
RUN pip install -r requirements.txt
COPY . /posmodelapp
ENTRYPOINT ["python"]
CMD ["run.py"]