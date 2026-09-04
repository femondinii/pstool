import socket
import sys
import ipaddress


def client(ip, port):
    ip_valid = ip_verify(ip)

    if ip_valid is None:
        print(f"[-] Invalid IP: {ip_valid}")
        return

    try:
        port = int(port)
    except ValueError:
        print(f"[-] Invalid port: {port}")
        return

    if not 1 <= port <= 65535:
        print("[-] Port must be between 1 and 65535.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((ip_valid, port))
        print(f"[+] {ip_valid}:{port} OPEN")

    except socket.timeout:
        print(f"[!] {ip_valid}:{port} TIMEOUT")

    except ConnectionRefusedError:
        print(f"[-] {ip_valid}:{port} CLOSED")

    except OSError as error:
        print(f"[!] Error: {error}")

    finally:
        sock.close()


def ip_verify(ip):
    try:
        ip_valid = ipaddress.ip_address(ip)
        return str(ip_valid)
    except ValueError:
        return None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Erro: Argumentos insuficientes.")
        print(f"Uso correto: python {sys.argv[0]} <IP_ADDRESS> <PORT>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = sys.argv[2]

    client(ip_address, port)