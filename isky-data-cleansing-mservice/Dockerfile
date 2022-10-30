# Dockerfile
FROM python:3.9
COPY requirements.txt /cleansingapp/requirements.txt
WORKDIR /cleansingapp
RUN pip install -r requirements.txt
COPY . /cleansingapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]