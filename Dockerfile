FROM python:3.10-slim
WORKDIR /app

RUN pip install --upgrade pip 

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh /app/
