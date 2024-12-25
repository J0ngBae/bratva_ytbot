FROM python:3.10.12-alpine

RUN apk add python3

COPY main.py .
COPY yt_util.py .
COPY cogs .
COPY config.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

CMD ["python", "main.py"]