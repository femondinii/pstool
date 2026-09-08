import socket

from models.scan_result import ScanResult
from scanner.base import BaseScanner


class TCPScanner(BaseScanner):

    def __init__(self, ip, timeout=1):
        super().__init__(ip)
        self.timeout = timeout

    def _scan(self, port):
        if self.ip is None:
            print("[-] Invalid IP.")
            return

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(self.timeout)

        try:
            client.connect((self.ip, port))
            service = socket.getservbyport(port)

            return ScanResult(port, "tcp", "open", service)

        except (socket.timeout, ConnectionRefusedError, OSError):
            return None

        finally:
            client.close()