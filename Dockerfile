FROM python:3.12.13-alpine3.23@sha256:7747d47f92cfca63a6e2b50275e23dba8407c30d8ae929a88ddd49a5d3f2d331

WORKDIR /app

RUN apk add --no-cache zlib~=1.3.2-r0 && apk add --no-cache openssl~=3.5.6-r0

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ARG PORT=8000
ENV PORT=${PORT}

EXPOSE ${PORT}

RUN mkdir -p /app/server/logs && addgroup -g1000 app && adduser -u 1000 -G app -s /sbin/nologin -D app && chown -R app:app /app
USER app

CMD ["python", "./main.py"]