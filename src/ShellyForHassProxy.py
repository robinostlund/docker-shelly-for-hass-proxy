import os
import socket
import struct

def shelly_proxy(hass_ip, hass_port, udp_ip, udp_port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind(('', udp_port))
  mreq = struct.pack("4sl", socket.inet_aton(udp_ip), socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  while True:
    try:
      # Receive CoAP message
      data, addr = sock.recvfrom(10240)
      # Debug
      print(data)
      print(addr)
      # Tag and add device ip-address to message
      newdata = bytearray(b'prxy')
      newdata.extend(socket.inet_aton(addr[0]))
      newdata.extend(data)
      # Send to Shelly plugin
      sock.sendto(newdata, (hass_ip, hass_port))
    except Exception as e:
      print ('exception ' + str(e))

def main():
  shelly_proxy(
    os.getenv('HOMEASSISTANT_IP'),
    int(os.getenv('HOMEASSISTANT_PORT')),
    os.getenv('PROXY_UDP_IP'),
    int(os.getenv('PROXY_UDP_PORT'))
  )
if __name__ == '__main__':
  main()