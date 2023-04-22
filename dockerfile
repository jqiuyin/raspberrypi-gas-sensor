FROM arm32v7/python:3.7.3
WORKDIR /app
RUN pip install RPi.GPIO
COPY mq-135.py ./
CMD ["python3", "mq-135.py"]