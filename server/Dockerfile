FROM debian:stable
FROM python:3.9
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y openssl
RUN adduser backvenom
USER backvenom
WORKDIR /home/backvenom
COPY --chown=backvenom:backvenom . .
RUN pip install --user -r requirements.txt
ENV PATH="/home/backvenom/.local/bin:${PATH}"
ENV PYTHONPATH="$PYTHONPATH:/home/backvenom/venomsrc"
CMD bash venomsrc/ssl/gen_selfsigned.sh