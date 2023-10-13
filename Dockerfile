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

# docker build . -t bobo:0.3
# docker run -it -p 5000:5000 bobo:0.3 /bin/sh
# docker run -it -p 5000:5000 bobo:0.3