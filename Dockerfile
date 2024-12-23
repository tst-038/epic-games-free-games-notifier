# Use a base image with Python
FROM python:3.10-slim

# Set environment variables
ENV PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY . .

# Install Playwright and required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install
RUN playwright install-deps

# Set the entry point
CMD ["python", "main.py"]