FROM python:3.9.7-bullseye

RUN mkdir /opt/csc-cinemabot
COPY requirements.txt /opt/csc-cinemabot
RUN pip install -r /opt/csc-cinemabot/requirements.txt &&\
    rm /opt/csc-cinemabot/requirements.txt
ENTRYPOINT /bin/bash

# ENV SBIS_TEST_ENV_PATH="/root/test_env/"
# ENV LD_LIBRARY_PATH="/root/test_env/"
# COPY terraform.py /root
# RUN python3 /root/terraform.py && rm /root/terraform.py
# RUN mkdir /root/requirements
# # На хосте в requirements должны лежать все необходимые для тестового
# # окружения пакеты из pip
# COPY requirements /root/requirements
# COPY requirements.txt /root
# COPY test_bl_config.ini /root/test_env/sbis-rpc-service.ini
# # Сюда будет примонтирована папка с тестами
# WORKDIR /root/test_env/modules/Retail/retail/tests
# ENTRYPOINT /usr/bin/bash