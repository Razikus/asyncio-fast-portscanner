# -*- coding: utf-8 -*-
import asyncio
import ipaddress
from typing import Sequence, Tuple

"""Main module."""


class FastPortScanner():
    def __init__(self, timeout: float, verboseLogging: str, hostList: Sequence[str] = [], portList: Sequence[int] = []):
        self.hostList = hostList
        self.portList = portList
        self.timeout = timeout
        self.verboseLogging = verboseLogging

    async def loadHostListByCidr(self, cidr: str) -> Tuple[bool, str]:
        self.hostList = []
        try:
            self.hostList = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
        except ipaddress.AddressValueError as e:
            return False, e
        except ipaddress.NetmaskValueError as e:
            return False, e
        except ValueError as e:
            return False, e
        if(len(self.hostList) <= 0):
            return False, "List of hosts is empty"

        return True, ""
    async def loadPortList(self, ports: Sequence[int]) -> Tuple[bool, str]:
        self.portList = []
        if(len(ports) == 0):
            return False, "0 length sequence"
        self.portList = ports
        return True, ""

    async def tcp_check(hostname: str, port: int) -> bool:
        try:
            reader, writer = await asyncio.open_connection(hostname, port)
            writer.close()
            return True
        except Exception as e:
            return False
        return True

    async def tcp_check_timeout(host: str, port: int, timeout: float) -> dict:
        try:
            return {"host": host, "status": await asyncio.wait_for(FastPortScanner.tcp_check(host, port), timeout=timeout), "port": port}
        except asyncio.TimeoutError:
            return {"host": host, "status": False, "port": port}

    async def gatherResults(self):
        tasks = []
        for host in self.hostList:
            for port in self.portList:
                tasks.append(FastPortScanner.tcp_check_timeout(host, port, self.timeout))
        print(self.portList)

        return await asyncio.gather(*tasks)

