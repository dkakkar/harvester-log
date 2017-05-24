FROM python:2.7.11

WORKDIR /usr/local/src/harvester-log

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Do this last; most likely to change
COPY src/harvester-logging.py ./

CMD ["python2","harvester-logging.py"]
