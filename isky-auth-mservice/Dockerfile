# Dockerfile
FROM python:3.9
COPY requirements.txt /authapp/requirements.txt
WORKDIR /authapp
RUN pip install -r requirements.txt
COPY . /authapp
ENTRYPOINT ["python"]
CMD ["run.py"]