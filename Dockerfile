FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV PYTHONPATH /app

EXPOSE 3000

CMD ["python", "bot.py"]