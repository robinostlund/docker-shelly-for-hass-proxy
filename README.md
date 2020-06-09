# Information
This is a docker container running shelly for hass proxy [ShellyForHass](https://github.com/StyraHem/ShellyForHASS)

If you are running shelly devices on different vlan or running home assistant in an emulated network environemnt on docker you can use this container to forward CoAP messages to ShellyForHASS Plugin.

On your home assistant container you need to add a port like this: 5684:5683/udp

Big thanks to [StyraHem.se](https://www.styrahem.se/c/126/shelly) for an awesome component to Home Assistant

----------
# Environment Variables
| Variable | Description | Default |
| :--- | :--- | :---  |
| HASS_IP | IP of your home assistant to forward packages to | 127.0.0.1 |
| HASS_PORT | Port for shelly in your home assistant | 5684|
| PROXY_IP | Shelly multicast address | 224.0.1.187 |
| PROXY_PORT | Shelly proxy port | 5683 |


----------
# Start ShellyForHassProxy container:
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