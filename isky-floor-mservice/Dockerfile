# Dockerfile
FROM python:3.9
COPY requirements.txt /floorapp/requirements.txt
WORKDIR /floorapp
RUN pip install -r requirements.txt
COPY . /floorapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]