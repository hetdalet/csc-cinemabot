FROM python:3.9.7-bullseye

# RUN mkdir /opt/csc-cinemabot
COPY requirements.txt /opt/csc-cinemabot/
COPY test_data /opt/csc-cinemabot/test_data/
COPY sources /opt/csc-cinemabot/sources/
COPY bot.py /opt/csc-cinemabot/
RUN pip install -r /opt/csc-cinemabot/requirements.txt &&\
    rm /opt/csc-cinemabot/requirements.txt
ENTRYPOINT /bin/bash
