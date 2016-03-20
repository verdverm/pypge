FROM verdverm/pypge-base

RUN sudo apt-get update \
	&& \
	sudo apt-get install -y --no-install-recommends \
	f2c \
	&& \
	/scripts/clean-apt.sh

WORKDIR /gocode

ENV GOPATH /gocode

RUN /usr/local/go/bin/go get -u github.com/gorilla/websocket

RUN mkdir -p gocode/src/github.com/verdverm/pypge/
ADD evaluator /gocode/src/github.com/verdverm/pypge/evaluator 

RUN cd /gocode/src/github.com/verdverm/pypge/evaluator/regress/levmar-2.6 && \
	cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLINSOLVERS_RETAIN_MEMORY=0 . && \
	make

RUN ls /gocode/src/github.com/verdverm/pypge/evaluator/regress/levmar-2.6

RUN cd /gocode/src/github.com/verdverm/pypge/evaluator && \
	ls regress && \
	/usr/local/go/bin/go install 

ENTRYPOINT ["/gocode/bin/evaluator"]

