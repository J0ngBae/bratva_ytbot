FROM python:3.10.12-alpine

RUN apk add --no-cache python3-dev gcc ffmpeg opus-dev musl-dev

RUN mkdir /bot
WORKDIR /bot

COPY main.py /bot
COPY yt_util.py /bot
COPY cogs/ /bot/cogs
COPY config.py /bot
COPY requirements.txt /bot
COPY local_music/ /bot/local_music

RUN pip install -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

CMD ["python", "main.py"]