import socket
from time import sleep

from models.scan_result import ScanResult
from scanner.base import BaseScanner


class UDPScanner(BaseScanner):

    def _scan(self, port):
        if self.ip is None:
            print("[-] Invalid IP.")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            client.sendto(b"PING\n", (self.ip, port))
            service = socket.getservbyport(port, 'udp')
            sleep(1)
            client.recvfrom(1024)

            return ScanResult(port, "udp", "open", service)
        except:
            return None

        finally:
            client.close()