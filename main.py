import argparse

from scanner.tcp import TCPScanner
from scanner.udp import UDPScanner


def main():
    parser = argparse.ArgumentParser(
        prog="pstool",
        description="Pentest Socket Toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # =========================
    # TCP
    # =========================

    tcp_parser = subparsers.add_parser(
        "tcp",
        help="TCP port scanning"
    )

    tcp_parser.add_argument(
        "ip",
        help="Target IP address"
    )

    tcp_parser.add_argument(
        "--port",
        type=int,
        help="Single TCP port"
    )

    tcp_parser.add_argument(
        "--ports",
        help="TCP port range (example: 8000-8100)"
    )

    # =========================
    # UDP
    # =========================

    udp_parser = subparsers.add_parser(
        "udp",
        help="UDP port scanning"
    )

    udp_parser.add_argument(
        "ip",
        help="Target IP address"
    )

    udp_parser.add_argument(
        "--port",
        type=int,
        help="Single UDP port"
    )

    udp_parser.add_argument(
        "--ports",
        help="UDP port range (example: 8000-8100)"
    )

    args = parser.parse_args()

    if args.command == "tcp":
        if args.port is None and args.ports is None:
            tcp_parser.error("You must specify --port or --ports.")

        if args.port is not None and args.ports is not None:
            tcp_parser.error("Use --port OR --ports, not both.")

        scanner = TCPScanner(args.ip)

        if args.port is not None:
            scanner.scan_port(args.port)

        elif args.ports is not None:
            try:
                port_ini, port_fin = args.ports.split("-")
            except ValueError:
                tcp_parser.error(
                    "Invalid port range. Use: --ports 8000-8100"
                )

            scanner.scan_range(port_ini, port_fin)
    elif args.command == "udp":
        if args.port is None and args.ports is None:
            tcp_parser.error("You must specify --port or --ports.")

        if args.port is not None and args.ports is not None:
            tcp_parser.error("Use --port OR --ports, not both.")

        scanner = UDPScanner(args.ip)

        if args.port is not None:
            scanner.scan_port(args.port)

        elif args.ports is not None:
            try:
                port_ini, port_fin = args.ports.split("-")
            except ValueError:
                tcp_parser.error(
                    "Invalid port range. Use: --ports 8000-8100"
                )

            scanner.scan_range(port_ini, port_fin)


if __name__ == "__main__":
    main()