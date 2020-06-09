# Shelly For Hass Proxy Container
This is a docker container image running ShellyForHASS proxy for Home Assisant component [ShellyForHass](https://github.com/StyraHem/ShellyForHASS)

If you are running shelly devices on different vlan or running home assistant in an emulated network environemnt on docker you can use this container to forward CoAP messages to ShellyForHASS Plugin.

## Thanks to
- [StyraHem.se](https://www.styrahem.se/c/126/shelly) for an awesome component to Home Assistant

## Installation

## Environment Variables
| Variable | Description | Default |
| :--- | :--- | :---  |
| HASS_IP | IP of your home assistant to forward packages to | 127.0.0.1 |
| HASS_PORT | Port for shelly in your home assistant | 5683|
| PROXY_IP | Shelly multicast address | 224.0.1.187 |
| PROXY_PORT | Shelly proxy port | 5683 |

## Start ShellyForHassProxy container:
:warning: **Important to use --net host**

```sh
$ docker run -dt \
    --name shellyforhassproxy \
    --hostname shelly_proxy \
    --net host \
    -e HASS_IP=127.0.0.1 \
    -e HASS_PORT=5684\
    -e PROXY_IP=224.0.1.187 \
    -e PROXY_PORT=5683 \
    robostlund/shelly-for-hass-proxy:latest
```

### Home Assistant
If you are running Home Assistant in a docker container with network mode bridge, then you need to set HASS_PORT to like 5684 and add port to your Home Assistant container like: 5684:5683/udp