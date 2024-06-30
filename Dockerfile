FROM python:3

ENV PYTHONUNBUFFERED=1

# Install necessary system packages, including tzdata
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone to Asia/Kolkata
ENV TZ=Asia/Kolkata


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt