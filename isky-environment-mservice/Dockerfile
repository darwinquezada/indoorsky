# Dockerfile
FROM python:3.9
COPY requirements.txt /envapp/requirements.txt
WORKDIR /envapp
RUN pip install -r requirements.txt
COPY . /envapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]