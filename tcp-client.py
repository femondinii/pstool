import socket
import sys
import ipaddress


def client(ip, port_ini, port_fin):
    ip_valid = ip_verify(ip)

    if ip_valid is None:
        print(f"[-] Invalid IP: {ip}")
        return

    try:
        port_ini = int(port_ini)
        port_fin = int(port_fin)
    except ValueError:
        print(f"[-] Invalid port")
        return

    if port_ini > port_fin:
        print("[-] The start port must be less than the end port.")
        return

    if not 1 <= port_ini <= 65535 or not 1 <= port_fin <= 65535:
        print("[-] Port must be between 1 and 65535.")
        return

    for port in range(port_ini, port_fin + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((ip_valid, port))
            print(f"[+] tcp/{port} OPEN")
        except socket.timeout:
            print(f"[!] tcp/{port} TIMEOUT")
        except ConnectionRefusedError:
            print(f"[-] tcp/{port} CLOSED")
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
    if len(sys.argv) < 4:
        print("Erro: Argumentos insuficientes.")
        print(f"Uso correto: python {sys.argv[0]} <IP_ADDRESS> <PORT>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port_ini = sys.argv[2]
    port_fin = sys.argv[3]

    client(ip_address, port_ini, port_fin)