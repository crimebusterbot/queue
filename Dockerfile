FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install -qq -y \
        build-essential \
        libffi-dev \
        python3-dev \
        openssl
RUN mkdir -p /app
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install pip --upgrade --force-reinstall \
    && pip3 install -r /app/requirements.txt
ADD . /app
# set environment variables
# RUN python3 set_env.py
CMD ["gunicorn", "app:app", "--bind", "0:8081"]
