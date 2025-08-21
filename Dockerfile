FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Make run.sh executable
RUN chmod +x /app/run.sh

EXPOSE 8000

# Start server using run.sh
CMD ["/app/run.sh"]
