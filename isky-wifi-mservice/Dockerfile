# Dockerfile
FROM python:3.9
COPY requirements.txt /wifiapp/requirements.txt
WORKDIR /wifiapp
RUN pip install -r requirements.txt
COPY . /wifiapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]