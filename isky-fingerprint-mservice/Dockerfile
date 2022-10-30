# Dockerfile
FROM python:3.9
COPY requirements.txt /fingerprintapp/requirements.txt
WORKDIR /fingerprintapp
RUN pip install -r requirements.txt
COPY . /fingerprintapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]