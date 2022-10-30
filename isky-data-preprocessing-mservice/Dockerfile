# Dockerfile
FROM python:3.9
COPY requirements.txt /preprocessingapp/requirements.txt
WORKDIR /preprocessingapp
RUN pip install -r requirements.txt
COPY . /preprocessingapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]