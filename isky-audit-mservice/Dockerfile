# Dockerfile
FROM python:3.9
COPY requirements.txt /auditapp/requirements.txt
WORKDIR /auditapp
RUN pip install -r requirements.txt
COPY . /auditapp
ENTRYPOINT ["python"]
CMD ["run.py"]