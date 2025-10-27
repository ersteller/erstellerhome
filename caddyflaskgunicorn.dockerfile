FROM ubuntu:25.10

# ------------------------
# System-Abhängigkeiten
# ------------------------
RUN apt update && apt install -y \
    python3 python3-venv curl ca-certificates gpg

# ------------------------
# Python / Flask / Gunicorn
# ------------------------
RUN python3 -m venv /opt/flask
RUN /opt/flask/bin/pip install --upgrade pip
RUN /opt/flask/bin/pip install flask markdown gunicorn requests

# ------------------------
# install Caddy 
# ------------------------
    # apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && chmod o+r /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && chmod o+r /etc/apt/sources.list.d/caddy-stable.list \
    && apt update \
    && apt install -y caddy 

ENV PATH="/opt/flask/bin:$PATH"
ENV FLASK_APP=src.server
ENV FLASK_ENV=production

WORKDIR /app
COPY src src
COPY site site
COPY styles styles
COPY img img
COPY README.md ./

# copy Caddyfile
COPY src/Caddyfile /etc/caddy/Caddyfile

# ------------------------
# Startscript for Caddy + Gunicorn
# ------------------------
# COPY startup.sh /startup.sh
RUN chmod +x src/startup.sh

EXPOSE 80 443 8000

CMD ["src/startup.sh"]


# docker build -t ucfimage -f caddyflaskgunicorn.dockerfile . 
# docker run -it -p 80:80 -p 443:443 ucfimage 

# -v ${PWD}:/app -p 8000:8000 # for development purposes
