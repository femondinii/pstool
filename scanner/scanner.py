from abc import ABC, abstractmethod
from utils.validations import validate_port, validate_ip


class BaseScanner(ABC):

    def __init__(self, ip):
        self.ip = validate_ip(ip)

    @abstractmethod
    def _scan(self, port):
        pass

    def scan_port(self, port):
        port = validate_port(port)

        if port is None:
            return

        self._scan(port)

    def scan_range(self, port_ini, port_fin):
        port_ini = validate_port(port_ini)
        port_fin = validate_port(port_fin)

        if port_ini is None or port_fin is None:
            return

        if port_ini > port_fin:
            print("[-] The start port must be less than the end port.")
            return

        for port in range(port_ini, port_fin + 1):
            self._scan(port)