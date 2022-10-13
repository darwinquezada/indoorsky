# Dockerfile
FROM python:3.9
COPY requirements.txt /userapp/requirements.txt
WORKDIR /userapp
RUN pip install -r requirements.txt
COPY . /userapp
ENTRYPOINT ["python"]
CMD ["run.py"]