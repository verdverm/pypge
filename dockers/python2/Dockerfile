FROM verdverm/pypge-base

RUN sudo apt-get update \
	&& \
	sudo apt-get install -y --no-install-recommends \
	libpng-dev \
	libfreetype6-dev \
	python-setuptools \
	python-dev \
	python-pip \
	&& \
	/scripts/clean-apt.sh

WORKDIR /pycode

COPY requirements.txt /pycode/requirements.txt
RUN pip install -r /pycode/requirements.txt

VOLUME /pycode
