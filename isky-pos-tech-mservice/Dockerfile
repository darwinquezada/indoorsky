# Dockerfile
FROM python:3.9
COPY requirements.txt /postech/requirements.txt
WORKDIR /postech
RUN pip install -r requirements.txt
COPY . /postech
ENTRYPOINT ["python"]
CMD ["run.py"]