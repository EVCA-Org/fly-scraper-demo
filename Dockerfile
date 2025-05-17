FROM python:3.11-slim

WORKDIR /app

# Install Chrome for headless browsing
RUN apt-get update && apt-get install -y     wget     gnupg     curl     unzip     && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -     && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list     && apt-get update && apt-get install -y     google-chrome-stable     && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for Chrome
ENV PYTHONUNBUFFERED=1     PYTHONDONTWRITEBYTECODE=1     CHROME_BIN=/usr/bin/google-chrome     CHROME_PATH=/usr/lib/chromium/

# Expose port 8080 for the health check endpoint
EXPOSE 8080

# Command to run your scraper
CMD [python, app.py]
