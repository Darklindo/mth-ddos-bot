FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Mth_Ddos_v50.py .

CMD ["python3", "Mth_Ddos_v50.py", "polling"]
