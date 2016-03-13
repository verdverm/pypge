# Use phusion/baseimage as base image. 
# See https://github.com/phusion/baseimage-docker
FROM phusion/baseimage:0.9.18
MAINTAINER Tony Worm verdverm@gmail.com

WORKDIR /root
ENV HOME /root

# Regenerate SSH host keys. baseimage-docker does not contain any
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]


### .........Custom Stuff............... ###

COPY dotfiles/profile /root/.myprofile
RUN echo "source /root/.myprofile" >> /root/.bashrc

# Add cleanup script
RUN mkdir /scripts
COPY scripts/clean-apt.sh /scripts/clean-apt.sh

# Update
RUN sudo apt-get update && sudo apt-get upgrade -y && /scripts/clean-apt.sh

# Install building tools
RUN sudo apt-get update \
	&& \
	sudo apt-get install -y --no-install-recommends \
	build-essential \
	cmake \
	gfortran \
	git \
	libblas3 \ 
	libblas-dev \
	liblapack3 \
	liblapack-dev \
	libyaml-0-2 \
	libyaml-dev \
	pkg-config \
	wget \
	&& \
	/scripts/clean-apt.sh

# install golang
RUN wget https://storage.googleapis.com/golang/go1.5.2.linux-amd64.tar.gz && \
	tar -C /usr/local -xzf go1.5.2.linux-amd64.tar.gz && \
	rm -f go1.5.2.linux-amd64.tar.gz && \
	echo "export PATH=$PATH:/usr/local/go/bin" >> /root/.bashrc

