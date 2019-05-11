FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV USERNAME queue
ENV PASSWORD 4J7o!ZFW^6
RUN apt-get update && \
    apt-get upgrade -qy && \
    apt-get install -qy \
        build-essential \
        libffi-dev \
        openssl \
        python3-dev
RUN mkdir -p /app
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install pip --upgrade --force-reinstall \
    && pip3 install -r /app/requirements.txt
ADD . /app
EXPOSE 5055
CMD ["python3", "app.py"]
