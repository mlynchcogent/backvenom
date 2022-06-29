#!/usr/bin/bash

filename=/home/backvenom/.env

sed -ci "s/^BACKVENOM_PASSWORD=$/BACKVENOM_PASSWORD=$(openssl rand -base64 6)/g" $filename
sed -ci "s/^ELASTIC_PASSWORD=$/ELASTIC_PASSWORD=$(openssl rand -base64 6)/g" $filename

pass=$(openssl rand -base64 10)

openssl genrsa -des3 -passout pass:${pass} -out server.pass.key 2048 && \
openssl rsa -passin pass:${pass} -in server.pass.key -out private.key && \
rm server.pass.key && \
openssl req -new -key private.key -out server.csr \
    -subj "/C=RU/CN=backvenom" && \
openssl x509 -req -days 365 -in server.csr -signkey private.key -out venom.crt

python venomsrc/endpoints/raw_server/asynserver.py
