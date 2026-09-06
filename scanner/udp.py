import socket
from time import sleep

from scanner.scanner import BaseScanner


class UDPScanner(BaseScanner):

    def __init__(self, ip):
        super().__init__(ip)

    def _scan(self, port):
        if self.ip is None:
            print("[-] Invalid IP.")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            client.sendto(b"PING\n", (self.ip, port))
            sleep(1)
            client.recvfrom(1024)
            print(f"[+] udp/{port} OPEN")
        except:
            print(f"[-] udp/{port} CLOSED")
            client.close()
        finally:
            client.close()