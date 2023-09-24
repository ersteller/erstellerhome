FROM python 

RUN pip install flask markdown
RUN echo exit > /root/.bash_history
RUN echo python /app/src/server.py >> /root/.bash_history
WORKDIR /app


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

