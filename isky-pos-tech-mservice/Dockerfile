# Dockerfile
FROM python:3.9
COPY requirements.txt /postech/requirements.txt
WORKDIR /postech
RUN pip install -r requirements.txt
COPY . /postech
RUN chmod +x boot.sh
ENV FLASK_APP run.py
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]