FROM alpine:latest

RUN apk add --update --no-cache \
	python3 \ 
	py3-pip \
	ffmpeg \
	git
# youtube-dl is install via git

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY .env ./

EXPOSE 5000

CMD python main.py
