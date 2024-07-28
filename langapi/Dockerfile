FROM python:3.11

WORKDIR /requirements
ADD requirements.txt ./
RUN pip install -r requirements.txt

ENV PYTHONPYCACHEPREFIX /tmp
# ENV PYTHONDONTWRITEBYTECODE true

WORKDIR /app
# ENTRYPOINT ["/usr/bin/bash", "autoreload-entrypoint.sh"]
