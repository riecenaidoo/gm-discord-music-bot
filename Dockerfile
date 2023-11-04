FROM python:3.10-alpine

RUN apk update && apk upgrade
RUN apk add ffmpeg git
    # youtube-dl is install via git

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY .env ./

EXPOSE 5000

CMD python main.py