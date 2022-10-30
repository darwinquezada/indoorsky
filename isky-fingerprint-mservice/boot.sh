#!/bin/sh

# go to directory where the app is
cd /fingerprintapp
# start gunicorn
exec gunicorn --bind :5000 run:app --certfile ./certs/cert.pem --keyfile ./certs/privkey.pem