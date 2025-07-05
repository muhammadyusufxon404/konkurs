FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["/opt/venv/bin/python", "main.py"]
