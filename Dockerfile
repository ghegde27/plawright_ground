
FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget gnupg2 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 libxrandr2 libxss1 libasound2 libgbm1 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install pytest pytest-asyncio playwright allure-pytest

# Install browsers with playwright
RUN playwright install --with-deps

WORKDIR /app
COPY . /app

CMD ["pytest", "--alluredir=allure-results", "-vv", "-n1"]
