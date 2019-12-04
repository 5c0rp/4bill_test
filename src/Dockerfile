FROM python:3.6

RUN python -m pip install --upgrade pip

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

COPY . /app

WORKDIR /app

EXPOSE 5000

ENTRYPOINT /docker-entrypoint.sh