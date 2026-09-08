import argparse
import time

from rich.console import Console
from rich.table import Table

from scanner.tcp import TCPScanner
from scanner.udp import UDPScanner
from scanner.ssh import SSHClient


VERSION = "1.0.0"

console = Console()


def print_banner():
    console.print()
    console.print(f"[bold]PSTool {VERSION}[/bold]")
    console.print("Pentest Socket Toolkit")
    console.print()


def print_scan_info(ip, protocol, port_range):
    console.print(f"[bold]Target:[/bold]   {ip}")
    console.print(f"[bold]Protocol:[/bold] {protocol.upper()}")
    console.print(f"[bold]Ports:[/bold]    {port_range}")
    console.print()


def print_table(results):

    table = Table(title="Scan Results")

    table.add_column("PORT", style="cyan")
    table.add_column("STATE")
    table.add_column("SERVICE")

    for result in results:

        if result.state == "open":
            state = "[green]open[/green]"
        else:
            state = result.state

        table.add_row(
            f"{result.port}/{result.protocol}",
            state,
            result.service
        )

    console.print(table)
    console.print()


def print_summary(results, total_ports, elapsed_time):

    console.print(
        f"[green]{len(results)} open port(s) found[/green]"
    )

    console.print(
        f"{total_ports} port(s) scanned"
    )

    console.print(
        f"Scan completed in {elapsed_time:.2f} seconds"
    )

    console.print()


def add_scan_arguments(parser):

    parser.add_argument(
        "ip",
        help="Target IP address"
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Single port"
    )

    parser.add_argument(
        "--ports",
        help="Port range (example: 8000-8100)"
    )


def run_scan(scanner, args, parser):

    if args.port is None and args.ports is None:
        parser.error("You must specify --port or --ports.")

    if args.port is not None and args.ports is not None:
        parser.error("Use --port OR --ports, not both.")

    start_time = time.time()

    if args.port is not None:

        port_range = str(args.port)

        print_scan_info(
            args.ip,
            args.command,
            port_range
        )

        result = scanner.scan_port(args.port)

        results = []

        if result:
            results.append(result)

        total_ports = 1

    else:

        try:
            port_start, port_end = args.ports.split("-")

            port_start = int(port_start)
            port_end = int(port_end)

        except ValueError:
            parser.error(
                "Invalid port range. Use: --ports 8000-8100"
            )

        if port_start > port_end:
            parser.error(
                "The start port must be less than the end port."
            )

        print_scan_info(
            args.ip,
            args.command,
            f"{port_start}-{port_end}"
        )

        results = scanner.scan_range(
            port_start,
            port_end
        )

        total_ports = port_end - port_start + 1

    elapsed_time = time.time() - start_time

    print_table(results)

    print_summary(
        results,
        total_ports,
        elapsed_time
    )


def run_ssh(args):

    ssh = SSHClient(
        args.ip,
        args.username,
        args.password
    )

    try:

        console.print(
            f"Connecting to {args.ip}:22..."
        )

        ssh.connect()

        console.print(
            "[green][+] SSH connection established[/green]"
        )

        console.print()

        while True:

            command = input("ssh> ")

            if command.lower() in ("exit", "quit"):
                break

            ssh.execute(command)

    except Exception as exc:

        console.print(
            f"[red][-] SSH connection error: {exc}[/red]"
        )

    finally:

        ssh.close()


def main():

    parser = argparse.ArgumentParser(
        prog="pstool",
        description="Pentest Socket Toolkit"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # TCP

    tcp_parser = subparsers.add_parser(
        "tcp",
        help="TCP port scanning"
    )

    add_scan_arguments(tcp_parser)

    # UDP

    udp_parser = subparsers.add_parser(
        "udp",
        help="UDP port scanning"
    )

    add_scan_arguments(udp_parser)

    # SSH

    ssh_parser = subparsers.add_parser(
        "ssh",
        help="SSH client"
    )

    ssh_parser.add_argument(
        "ip",
        help="Target IP address"
    )

    ssh_parser.add_argument(
        "-u",
        "--username",
        required=True,
        help="SSH username"
    )

    ssh_parser.add_argument(
        "-p",
        "--password",
        required=True,
        help="SSH password"
    )

    args = parser.parse_args()

    print_banner()

    if args.command == "tcp":

        run_scan(
            TCPScanner(args.ip),
            args,
            tcp_parser
        )

    elif args.command == "udp":

        run_scan(
            UDPScanner(args.ip),
            args,
            udp_parser
        )

    elif args.command == "ssh":

        run_ssh(args)


if __name__ == "__main__":
    main()