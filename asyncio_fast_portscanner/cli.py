# -*- coding: utf-8 -*-

"""Console script for asyncio_fast_portscanner."""
import sys
import click
from .asyncio_fast_portscanner import FastPortScanner
import asyncio
import json
import itertools

@click.group()
def main():
    sys.exit(1)


@main.command()
@click.argument("range", type=click.STRING)
@click.argument("ports", nargs=-1, metavar="ports", type=click.IntRange(min=0, max=65535))
@click.option("--timeout", "-t", default=0.3, help="Specifies timeout", type=click.FLOAT)
@click.option("--outputformat", "-f", default="JSON",
              help="Specifies output format. \nFor json: \n{'host': host, 'ports': { 22: true, 33: false}}",
              type=click.Choice(["JSON", "TEXT"], case_sensitive=False))
@click.option("--sockettype", "-s", default="TCP", help="Specifies TCP or UDP type",
              type=click.Choice(["TCP", "UDP"], case_sensitive=False))
@click.option("--rangetype", "-r", default="cidr", help="Specifies type of range",
              type=click.Choice(["CIDR", "RANGE"], case_sensitive=False))
@click.option("--verbose", "-v", default=False, is_flag=True)
@click.option("--activeOnly", "-a", default=True, is_flag=True, help="Returns if at least one of the port is active, default true")
def scan(range: str, ports, timeout, outputformat: str, sockettype: str, rangetype: str, verbose: bool, activeonly: bool):
    """Scans for hosts in specified range.

    Range in CIDR format like 192.168.1.1/24
    So for example 192.168.1.0/24 gives 192.168.1.0 - 192.168.1.255 results

    Range in RANGE format like 192.168.1.0-255
    So for example 192.168.1.0-255 gives 192.168.1.0 - 192.168.1.255 results

    Range in RANGE format like 192.168.1-2.0-255
    This example produces 192.168.1.0 - 192.168.1.255 and 192.168.2.0 - 192.168.2.255 results

    For bigger bunch of tasks you have to increase timeout, because it will always report as Closed (because task
    will never have a chance to execute = timeout)

    For example for scan 192.168.0-255.0-255 22 -r RANGE -v -t 5 - timeout of 10 seconds is enough

    """
    loop = asyncio.get_event_loop()
    scanner = FastPortScanner(timeout, verbose)
    if rangetype.upper() == "CIDR":
        result = loop.run_until_complete(scanner.loadHostListByCidr(range))
        if not result[0]:
            conditionalClickEcho(verbose, result[1])
            sys.exit(1)
    elif rangetype.upper() == "RANGE":
        result = loop.run_until_complete(scanner.loadHostListByRange(range))
        if not result[0]:
            conditionalClickEcho(verbose, result[1])
            sys.exit(1)

    result = loop.run_until_complete(scanner.loadPortList(ports))
    if not result[0]:
        conditionalClickEcho(verbose, result[1])
        sys.exit(1)

    results = loop.run_until_complete(scanner.gatherResults())
    grouped = groupResults(results, activeonly)
    if(outputformat == "JSON"):
        click.echo(json.dumps(grouped))
    elif(outputformat == "TEXT"):
        for item in grouped:
            print(item, end = "; ")
            for port in grouped[item]["ports"]:
                if(grouped[item]["ports"][port]):
                    print(str(port), "Open", end = "; ")
                else:
                    print(str(port), "Closed", end = "; ")
            print()




def conditionalClickEcho(verbose, message):
    if verbose:
        click.echo(message)




def groupResults(result, activeOnly):
    grouped = dict()
    for obj in result:
        host = obj["host"]
        port = obj["port"]
        status = obj["status"]
        if host in grouped:
            grouped[host]["ports"][port] = status
        else:
            grouped[host] = dict()
            grouped[host]["ports"] = {port: status}

    if(activeOnly):
        toRemove = [key for key in grouped if not checkForActive(grouped[key]["ports"])]
        for key in toRemove: del grouped[key]

    return grouped

def checkForActive(portsStatus):
    for key in portsStatus:
        if(portsStatus[key]):
            return True
    return False


if __name__ == "__main__":
    main()  # pragma: no cover
