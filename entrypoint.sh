#!/bin/sh -e

if [ "${DEBUG}" == "true" ]; then
  set -x
fi

# get environment variables and set default ones
HOMEASSISTANT_IP=${HASS_IP:=127.0.0.1}
HOMEASSISTANT_PORT=${HASS_PORT:=5683}
PROXY_UDP_IP=${PROXY_IP:=224.0.1.187}
PROXY_UDP_PORT=${PROXY_PORT:=5683}
PROXY_DEBUG=${PROXY_DEBUG:=no}

# set environment variables
export HOMEASSISTANT_IP HOMEASSISTANT_PORT PROXY_UDP_IP PROXY_UDP_PORT PROXY_DEBUG

# start proxy
python3 /opt/proxy.py