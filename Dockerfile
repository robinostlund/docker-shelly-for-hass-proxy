FROM alpine:latest

RUN apk add --no-cache python3

ADD entrypoint.sh /opt/entrypoint.sh
ADD src/ShellyForHassProxy.py /opt/proxy.py

RUN chmod +x /opt/entrypoint.sh

#ENTRYPOINT ["/opt/entrypoint.sh"]
ENTRYPOINT ["python3 /opt/proxy.py"]