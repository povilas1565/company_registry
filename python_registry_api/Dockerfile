FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ./app

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc


COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy --ignore-pipfile

ENV POSTGRES_USER=registry
ENV POSTGRES_PASSWORD=supersecretpassword
ENV POSTGRES_DB=registry-dev


# Install application into container
COPY . .
EXPOSE 5000
ENTRYPOINT []

