FROM python:3.12-slim

WORKDIR /app

#install praw and requests
RUN pip install praw requests

COPY . .

CMD ["python", "using_praw.py"]