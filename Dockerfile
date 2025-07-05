FROM python:3.11-slim

# C compiler va kerakli kutubxonalarni o‘rnatamiz
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    && apt-get clean

ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH

COPY . /app/.
WORKDIR /app

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["/opt/venv/bin/python", "main.py"]
