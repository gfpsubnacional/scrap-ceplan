FROM python:3.10-slim

RUN apt-get update && apt-get install -y     wget     unzip     curl     gnupg     ca-certificates     chromium     chromium-driver     && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin/chromium:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
