# Dockerfile
FROM python:3.9
COPY requirements.txt /authapp/requirements.txt
WORKDIR /authapp
RUN pip install -r requirements.txt
COPY . /authapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]