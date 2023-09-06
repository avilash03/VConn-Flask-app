FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/requirements.txt


# Install system dependencies
RUN apt-get update && \
    apt-get install -y libmariadb-dev-compat libmariadb-dev gcc pkg-config && \
    rm -rf /var/lib/apt/lists/*






# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY . /app

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "application:application"]

