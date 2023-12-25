FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ./app

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc


COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy --ignore-pipfile


# Install application into container
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:./python_registry_api/"
ENV TEST False
EXPOSE 5001
ENTRYPOINT []

