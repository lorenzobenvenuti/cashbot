FROM easypi/alpine-arm

RUN [ "cross-build-start" ]

RUN apk add --update python py-pip

ADD *.py /src/
ADD requirements.txt /src/

WORKDIR /src
RUN pip install -r requirements.txt

RUN [ "cross-build-end" ]

CMD ["python", "cashbot.py", "/config/config.yml"]
