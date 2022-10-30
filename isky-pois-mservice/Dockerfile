# Dockerfile
FROM python:3.9
COPY requirements.txt /poiapp/requirements.txt
WORKDIR /poiapp
RUN pip install -r requirements.txt
COPY . /poiapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]