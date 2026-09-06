import socket

from scanner.scanner import BaseScanner


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
            print(f"[+] tcp/{port} OPEN")
        except socket.timeout:
            print(f"[!] tcp/{port} TIMEOUT")
        except ConnectionRefusedError:
            print(f"[-] tcp/{port} CLOSED")
        except OSError as error:
            print(f"[!] tcp/{port} ERROR: {error}")
        finally:
            client.close()