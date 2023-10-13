FROM debian:buster-slim

RUN apt-get update
RUN apt-get install -y python3.10 python3-pip ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

EXPOSE 5000

CMD ["python3" "main.py"]
