# Use the pre-configured official image
FROM python:3.12-alpine

WORKDIR /app

# Official images already have pip upgraded and ready
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]