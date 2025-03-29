FROM python:3.12
COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y nodejs npm && \
    pip install -r requirements.txt

COPY . ./
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]