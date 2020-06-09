import argparse
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
      # Tag and add device ip-address to message
      newdata = bytearray(b'prxy')
      newdata.extend(socket.inet_aton(addr[0]))
      newdata.extend(data)
      # Send to Shelly plugin
      sock.sendto(newdata, (hass_ip, hass_port))
    except Exception as e:
      print ('exception ' + str(e))

def main():
  parser = argparse.ArgumentParser(description='ShellyForHass Proxy.')
  parser.add_argument('--hass-ip', dest="hass_ip", type=str, help='Home Assistant IP', required=True)
  parser.add_argument('--hass-port', dest='udp_port', type=str, action='store', help="Home Assistant Port", required=True)
  parser.add_argument('--proxy-ip', dest="udp_ip", type=str, help='Shelly For Hass Proxy IP', required=True)
  parser.add_argument('--proxy-port', dest='udp_port', type=str, action='store', help="Shelly For Hass Proxy Port", required=True)
  args = parser.parse_args()

  shelly_proxy(
    args.hass_ip,
    int(args.hass_port),
    args.udp_ip,
    int(args.udp_port)
  )

if __name__ == '__main__':
  main()