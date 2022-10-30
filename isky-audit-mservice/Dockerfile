# Dockerfile
FROM python:3.9
COPY requirements.txt /auditapp/requirements.txt
WORKDIR /auditapp
RUN pip install -r requirements.txt
COPY . /auditapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]