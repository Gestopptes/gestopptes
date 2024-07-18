FROM python:3.12

WORKDIR /pipfiles
RUN pip install pipenv
ADD Pipfile Pipfile.lock ./
RUN  pipenv install --system --deploy --ignore-pipfile

ENV PYTHONPYCACHEPREFIX /tmp
ENV PYTHONDONTWRITEBYTECODE true

WORKDIR /app