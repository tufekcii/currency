FROM python:latest

WORKDIR /usr/src/app .

COPY requirements.txt .
COPY currency_api.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","./currency_api.py"]
