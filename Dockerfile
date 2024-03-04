FROM python:3.9

RUN adduser --disabled-password --gecos '' ml-api-user

WORKDIR /app

COPY ./serve /app/serve
COPY ./prediction_delivery_time /app/prediction_delivery_time
COPY pyproject.toml /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

RUN chmod +x /app/serve/run.sh
RUN chown -R ml-api-user:ml-api-user ./

EXPOSE 8001

CMD ["bash", "./serve/run.sh"]

