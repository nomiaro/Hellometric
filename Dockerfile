# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install google-api-core==2.7.3
RUN pip install google-auth==2.6.2
RUN pip install googleapis-common-protos==1.56.0
RUN pip install prometheus-client==0.14.1
RUN pip install prometheus-flask-exporter==0.20.1
RUN pip install requests==2.27.1


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app