FROM python:3.10

WORKDIR /code

COPY . /code

RUN chmod +x /code/setup.sh

RUN /code/setup.sh

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
