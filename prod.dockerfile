FROM python:3.9.7-bullseye

COPY requirements.txt /opt/csc-cinemabot/
COPY app /opt/csc-cinemabot/app/
RUN pip install -r /opt/csc-cinemabot/requirements.txt &&\
    rm /opt/csc-cinemabot/requirements.txt
ENTRYPOINT python3 /opt/csc-cinemabot/app/bot.py
