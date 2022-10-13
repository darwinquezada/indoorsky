# Dockerfile
FROM python:3.9
COPY requirements.txt /fingerprintapp/requirements.txt
WORKDIR /fingerprintapp
RUN pip install -r requirements.txt
COPY . /fingerprintapp
ENTRYPOINT ["python"]
CMD ["run.py"]