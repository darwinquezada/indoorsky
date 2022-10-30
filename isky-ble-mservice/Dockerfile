# Dockerfile
FROM python:3.9
COPY requirements.txt /bleapp/requirements.txt
WORKDIR /bleapp
RUN pip install -r requirements.txt
COPY . /bleapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]