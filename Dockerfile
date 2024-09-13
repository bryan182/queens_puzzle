FROM python:3.12-slim

WORKDIR /queens

COPY . /queens

RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install -r requirements.txt

CMD ["pytest", "-v"]