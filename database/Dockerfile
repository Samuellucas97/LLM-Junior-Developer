FROM python:3.11-slim

WORKDIR /app

RUN pip install dotenv pymongo

COPY db_setup.py /app/db_setup.py

CMD ["python", "/app/db_setup.py"]
