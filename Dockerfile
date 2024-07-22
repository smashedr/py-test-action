FROM python:3.11-alpine

COPY src/ /src

ENTRYPOINT ["python", "/src/main.py"]
