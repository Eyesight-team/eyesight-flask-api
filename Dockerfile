FROM python:3.13.1

WORKDIR /app

COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]