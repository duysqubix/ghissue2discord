FROM python:3.11 as requirements-stage 
WORKDIR /tmp 
RUN pip install poetry==1.4.0
COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export --output /tmp/requirements.txt --without-hashes
RUN cat /tmp/requirements.txt


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--reload"]