FROM python:3.12
RUN pip install Flask requests pymongo
ADD proxy.py ./
CMD flask --app proxy run --host=0.0.0.0