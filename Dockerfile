FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# встановлюємо залежності для підключення python до postgresql
RUN apk add postgresql-client build-base postgresql-dev

# встановлюємо залежності для social-auth-app-django
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo

# -r показуєм з якого файлу потрібно встановити залежності
RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password app-user

USER app-user
