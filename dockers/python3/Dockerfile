FROM verdverm/pypge-base

RUN sudo apt-get update \
	&& \
	sudo apt-get install -y --no-install-recommends \
	libpng-dev \
	libfreetype6-dev \
	python3-setuptools \
	python3-dev \
	python3-pip \
	&& \
	/scripts/clean-apt.sh

WORKDIR /pycode

COPY requirements.txt /pycode/requirements.txt
RUN pip3 install -r /pycode/requirements.txt

VOLUME /pycode
