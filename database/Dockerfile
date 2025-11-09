FROM python:3.11-slim

WORKDIR /app

# Install pymongo package
RUN pip install pymongo

# Copy your Python script into the container
COPY db_setup.py /app/db_setup.py

# Run the script
CMD ["python", "/app/db_setup.py"]
