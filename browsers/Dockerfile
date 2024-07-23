FROM python:3.12

WORKDIR /pipfiles
RUN apt-get update -y && apt-get install -y inotify-tools libinotifytools0
RUN pip install pipenv
ADD Pipfile Pipfile.lock ./
RUN  pipenv install --system --deploy --ignore-pipfile

ENV PYTHONPYCACHEPREFIX /tmp
# ENV PYTHONDONTWRITEBYTECODE true

WORKDIR /app
# ENTRYPOINT ["/usr/bin/bash", "autoreload-entrypoint.sh"]