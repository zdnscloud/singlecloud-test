FROM python:3.7-alpine

WORKDIR /singlecloud-test

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "many_log.py"]
