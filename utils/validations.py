import ipaddress


def validate_ip(ip):
    try:
        return str(ipaddress.ip_address(ip))
    except ValueError:
        return None


def validate_port(port):
    try:
        port = int(port)
    except (ValueError, TypeError):
        return None

    if not 1 <= port <= 65535:
        return None

    return port