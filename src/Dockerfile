FROM python:3.9.21-alpine3.21 AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.9.21-alpine3.21

WORKDIR /app

COPY . .

COPY --from=build /install /usr/local

EXPOSE 5000

CMD ["python", "app.py"]
