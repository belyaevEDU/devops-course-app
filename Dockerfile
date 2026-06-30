FROM python:3.12.13-alpine3.23@sha256:601d3d3797e90e2534782e69c85fafb7971b43f24c7b1b079b7e48dd435e458d

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip==26.1.1 && pip3 install --no-cache-dir -r requirements.txt

COPY /app .

ARG PORT=8000
ENV PORT=${PORT}

EXPOSE ${PORT}

RUN mkdir -p /app/server/logs && addgroup -g1000 app && adduser -u 1000 -G app -s /sbin/nologin -D app && chown -R app:app /app
USER app

CMD ["python", "./main.py"]