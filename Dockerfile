FROM python:3.12
COPY requirements.txt ./

RUN apt-get update && \
    apt-get install nodejs npm && \
    pip install -r requirements.txt && \
    npm install

COPY . ./
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "backend.server:app"]
