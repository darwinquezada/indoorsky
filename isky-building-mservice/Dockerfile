# Dockerfile
FROM python:3.9
COPY requirements.txt /buildingapp/requirements.txt
WORKDIR /buildingapp
RUN pip install -r requirements.txt
COPY . /buildingapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]