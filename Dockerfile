FROM python:3.10-alpine

RUN apk update && apk upgrade
RUN apk add ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

EXPOSE 5000

CMD ["python3" "main.py"]
