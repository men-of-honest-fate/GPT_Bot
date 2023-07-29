FROM python:3
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_NAME=ai_bot

COPY . /app
RUN pip install -U -r /app/requirements.txt

#CMD cd /app/Tor/TorBrowser/Tor
#CMD tor.exe
CMD python /app/main.py
