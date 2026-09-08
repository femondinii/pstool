from dataclasses import dataclass


@dataclass
class ScanResult:
    port: int
    protocol: str
    state: str
    service: str