FROM selenium/standalone-chrome:latest

USER root

# Install Python & pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget unzip && \
    ln -s /usr/bin/python3 /usr/bin/python

# Set matching ChromeDriver version
ENV CHROME_DRIVER_VERSION=136.0.7103.113

# Install compatible ChromeDriver manually
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64* chromedriver-linux64.zip

# Set Selenium offline mode and path to chromedriver
ENV SE_OFFLINE="false"
ENV PATH="/usr/local/bin:$PATH"
ENV webdriver.chrome.driver="/usr/local/bin/chromedriver"

# Set up working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Run your script
CMD ["python", "main.py"]