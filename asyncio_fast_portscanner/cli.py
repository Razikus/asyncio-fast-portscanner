# -*- coding: utf-8 -*-

"""Console script for asyncio_fast_portscanner."""
import sys
import click
import asyncio_fast_portscanner
import asyncio
import json


@click.group()
@click.pass_context
def main(ctx):
    return 1


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
@click.pass_context
def scan(ctx, range: str, ports, timeout, outputformat: str, sockettype: str, rangetype: str, verbose: bool, activeonly: bool):
    """Scans for hosts in specified range.

    Range in CIDR format like 192.168.1.1/24
    So for example 192.168.1.0/24 gives 192.168.1.0 - 192.168.1.255 results

    Range in RANGE format like 192.168.1.0-255
    So for example 192.168.1.0-255 gives 192.168.1.0 - 192.168.1.255 results

    Range in RANGE format like 192.168.1-2.0-255
    This example produces 192.168.1.0 - 192.168.1.255 and 192.168.2.0 - 192.168.2.255 results



    """
    loop = asyncio.get_event_loop()
    ctx.statusCode = 1
    scanner = asyncio_fast_portscanner.FastPortScanner(timeout, verbose)
    if rangetype.upper() == "CIDR":
        result = loop.run_until_complete(scanner.loadHostListByCidr(range))
        if not result[0]:
            conditionalClickEcho(verbose, result[1])
            return False
    elif rangetype.upper() == "RANGE":
        conditionalClickEcho(verbose, "Not supported yet")
        return False

    result = loop.run_until_complete(scanner.loadPortList(ports))
    if not result[0]:
        conditionalClickEcho(verbose, result[1])
        return False

    results = loop.run_until_complete(scanner.gatherResults())
    gruped = groupResults(results, activeonly)
    click.echo(json.dumps(gruped))


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
    sys.exit(main())  # pragma: no cover
