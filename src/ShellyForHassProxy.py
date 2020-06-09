import os
import socket
import struct

class ShellyProxy:
  def __init__(self, hass_ip, hass_port, udp_ip, udp_port, debug=None):
    self.hass_ip = hass_ip
    self.hass_port = hass_port
    self.udp_ip = udp_ip
    self.udp_port = udp_port
    self.debug = debug

  def run(self):
    # bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', self.udp_port))
    mreq = struct.pack("4sl", socket.inet_aton(self.udp_ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # start loop
    while True:
      try:
        # Receive CoAP message
        data, addr = sock.recvfrom(10240)
        # Debug
        if self.debug:
          print(data)
          print(addr)
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
  HOMEASSISTANT_IP = os.getenv('HOMEASSISTANT_IP')
  HOMEASSISTANT_PORT = int(os.getenv('HOMEASSISTANT_PORT'))
  PROXY_UDP_IP = os.getenv('PROXY_UDP_IP')
  PROXY_UDP_PORT = int(os.getenv('PROXY_UDP_PORT'))
  PROXY_DEBUG = os.getenv('PROXY_DEBUG', default=None)

  # start shelly proxy
  sp = ShellyProxy(HOMEASSISTANT_IP, HOMEASSISTANT_PORT, PROXY_UDP_IP, PROXY_UDP_PORT, PROXY_DEBUG)
  sp.run()

if __name__ == '__main__':
  main()
