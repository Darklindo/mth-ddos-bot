FROM python:3.11-slim

# Install system dependencies for dig, whois, traceroute
RUN apt-get update && apt-get install -y --no-install-recommends \
    dig dnsutils whois traceroute curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Mth_Ddos_v50.py .
COPY set_commands.py .

# Create data directory for DB and logs
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1

# Health check endpoint (bot exposes HTTP server on 8080)
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -sf http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["python3", "Mth_Ddos_v50.py"]
