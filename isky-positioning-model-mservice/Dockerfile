# Dockerfile
FROM python:3.9
COPY requirements.txt /posmodelapp/requirements.txt
WORKDIR /posmodelapp
RUN pip install -r requirements.txt
COPY . /posmodelapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]