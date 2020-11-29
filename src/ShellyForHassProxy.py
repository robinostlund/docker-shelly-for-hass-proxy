import os
import socket
import struct

from datetime import datetime 

class ShellyProxy:
  def __init__(self, hass_ip, hass_port, coap_ip, coap_port, debug=None):
    self.hass_ip = hass_ip
    self.hass_port = hass_port
    self.coap_ip = coap_ip
    self.coap_port = coap_port
    self.debug = debug

  def pprinter(self, msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] {msg}')

  def run(self):
    # bind socket
    self.pprinter(f'Starting ShellyForHASS Proxy..')
    self.pprinter(f'Listening on {self.coap_port} for messages from {self.coap_ip}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', self.coap_port))
    mreq = struct.pack("4sl", socket.inet_aton(self.coap_ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # start loop
    self.pprinter(f'Started ShellyForHASS Proxy and forwarding messages to {self.hass_ip}:{self.hass_port}')
    while True:
      try:
        # Receive CoAP message
        data, addr = sock.recvfrom(10240)
        # Debug
        if self.debug and self.debug == 'yes':
          self.pprinter(f'Got CoAP message from: {addr[0]}:{addr[1]}')
        # Tag and add device ip-address to message
        newdata = bytearray(b'prxy')
        newdata.extend(socket.inet_aton(addr[0]))
        newdata.extend(data)
        # Send to Shelly plugin
        sock.sendto(newdata, (self.hass_ip, self.hass_port))
      except Exception as e:
        print ('exception ' + str(e))


def main():
  # fetch variables
  HOMEASSISTANT_IP = os.getenv('HASS_IP')
  HOMEASSISTANT_PORT = int(os.getenv('HASS_PORT'))
  COAP_IP = os.getenv('COAP_IP')
  COAP_UDP_PORT = int(os.getenv('COAP_PORT'))
  PROXY_DEBUG = os.getenv('PROXY_DEBUG', default=None)

  # start shelly proxy
  sp = ShellyProxy(HOMEASSISTANT_IP, HOMEASSISTANT_PORT, COAP_IP, COAP_UDP_PORT, PROXY_DEBUG)
  sp.run()

if __name__ == '__main__':
  main()
