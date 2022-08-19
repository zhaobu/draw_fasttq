FROM python:3.10.6
# 创建和主机用户相同uid的用户，名为 liwei
RUN useradd --shell /bin/bash -u 2036 -o -c "" -m liwei \
    && usermod -a -G root liwei
WORKDIR /home/liwei/code/daily-works/python
# RUN pip install -r requirements.txt

