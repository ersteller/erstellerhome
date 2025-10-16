FROM python 

RUN pip install flask markdown
RUN echo exit > /root/.bash_history
RUN echo python /app/src/server.py >> /root/.bash_history
WORKDIR /app


COPY Dockerfile README.md ./
COPY src src
COPY site site
COPY styles styles
COPY img img
COPY .git .git

#ENV FLASK_ENV=development
ENV FLASK_ENV=production
ENV FLASK_APP=src/server

# CMD python src/server.py
CMD flask run --host=0.0.0.0 --port=80

RUN snap install --classic certbot

RUN ln -s /snap/bin/certbot /usr/bin/certbot

# if my website is not running
# RUN certbot certonly --standalone  
#if it was running (Docker build is not running the server)
# RUN certbot certonly --webroot

# try the renew 
# RUN certbot renew --dry-run



