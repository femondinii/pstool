from concurrent.futures import ThreadPoolExecutor, as_completed
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

        return self._scan(port)

    def scan_range(self, port_start, port_end):
        port_start = validate_port(port_start)
        port_end = validate_port(port_end)

        if port_start is None or port_end is None:
            return

        if port_start > port_end:
            print("[-] The start port must be less than the end port.")
            return

        results = []
        ports = range(port_start, port_end + 1)

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_port = {
                executor.submit(self._scan, port): port
                for port in ports
            }

            for future in as_completed(future_to_port):
                port = future_to_port[future]

                try:
                    result = future.result()

                    if result:
                        results.append(result)

                except Exception as err:
                    print(f"[-] Error scanning port {port}: {err}")

        return sorted(results, key=lambda result: result.port)