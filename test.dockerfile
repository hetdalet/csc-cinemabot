FROM csc-cinemabot:latest

ENV PYTHONPATH=/opt/csc-cinemabot/
RUN pip install pytest==6.2.5
RUN mkdir /opt/csc-cinemabot/tests
WORKDIR /opt/csc-cinemabot/tests
ENTRYPOINT /bin/bash
