# Dockerfile
FROM python:3.9
COPY requirements.txt /bleapp/requirements.txt
WORKDIR /bleapp
RUN pip install -r requirements.txt
COPY . /bleapp
ENTRYPOINT ["python"]
CMD ["run.py"]