FROM python:3.11-slim

WORKDIR /application/src

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

WORKDIR /application/src/src

CMD ["python", "main.py"]