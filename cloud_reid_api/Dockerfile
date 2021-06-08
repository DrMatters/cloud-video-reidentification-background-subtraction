FROM python:3.7

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS=/root/gcloud.json

EXPOSE 8080

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--port", "8080", "--log-level", "debug"]
