FROM arm32v7/python:3.7.3
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY mq-135.py ./
CMD ["python3", "mq-135.py"]