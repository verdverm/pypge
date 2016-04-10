# FROM alpine
FROM verdverm/pypge-python3

ADD . /pycode
RUN pip3 install .

