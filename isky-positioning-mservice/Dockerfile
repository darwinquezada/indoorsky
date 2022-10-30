# Dockerfile
FROM python:3.9
COPY requirements.txt /positioningapp/requirements.txt
WORKDIR /positioningapp
RUN pip install -r requirements.txt
COPY . /positioningapp
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]