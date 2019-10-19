# -*- coding: utf-8 -*-
import asyncio
import ipaddress
from typing import Sequence, Tuple
import itertools
import re

"""Main module."""


class FastPortScanner():
    def __init__(self, timeout: float, verboseLogging: bool = False, hostList: Sequence[str] = [],
                 portList: Sequence[int] = []):
        self.hostList = hostList
        self.portList = portList
        self.timeout = timeout
        self.verboseLogging = verboseLogging

    async def loadHostListByCidr(self, cidr: str) -> Tuple[bool, str]:
        self.hostList = []
        try:
            self.hostList = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
            if (self.verboseLogging):
                print("Hostlist:", self.hostList)
        except ipaddress.AddressValueError as e:
            return False, e
        except ipaddress.NetmaskValueError as e:
            return False, e
        except ValueError as e:
            return False, e
        if (len(self.hostList) <= 0):
            return False, "List of hosts is empty"

        return True, ""

    async def loadPortList(self, ports: Sequence[int]) -> Tuple[bool, str]:
        self.portList = []
        if (len(ports) == 0):
            return False, "0 length sequence"
        self.portList = ports
        if (self.verboseLogging):
            print("Hostlist:", self.portList)
        return True, ""

    # This shit is to refactor, cause i can't invent anything better now :D


    async def loadHostListByRange(self, rangeString: str) -> Tuple[bool, str]:
        splitted = rangeString.split(".")
        hostList = []
        indexes = []
        lists = []
        index = 0
        for piece in splitted:
            if ("-" in piece):
                pieceSplitted = piece.split("-")
                minimum = int(pieceSplitted[0])
                maximum = int(pieceSplitted[1])
                if(minimum > maximum):
                    return False, "One of range is invalid (minimum > maximum)"

                lists.append([x for x in range(minimum, maximum + 1)])
                indexes.append(index)
            index = index + 1

        pipe = "-0-.-1-.-2-.-3-"
        for index in range(0, 4):
            if index not in indexes:
                pipe = pipe.replace("-" + str(index) + "-", splitted[index])

        if (len(indexes) > 0):
            products = itertools.product(*lists)
            for product in products:
                pipeFormat = pipe
                indexNow = 0
                for index in indexes:
                    pipeFormat = pipeFormat.replace("-" + str(index) + "-", str(product[indexNow]))
                    indexNow = indexNow + 1
                hostList.append(pipeFormat)
        else:
            hostList.append(pipe)

        ipRegex = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        for host in hostList:
            if(not ipRegex.match(host)):
                return False, host + " doesn't match ipv4 regex"

        if len(hostList) <= 0:
            return False, "List of hosts is empty"

        self.hostList = hostList
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
            return {"host": host,
                    "status": await asyncio.wait_for(FastPortScanner.tcp_check(host, port), timeout=timeout),
                    "port": port}
        except asyncio.TimeoutError:
            return {"host": host, "status": False, "port": port}


    async def gatherResults(self):
        tasks = []
        for host in self.hostList:
            for port in self.portList:
                if (self.verboseLogging):
                    print("Preparing task for " + host + ":" + str(port) + "...")
                tasks.append(FastPortScanner.tcp_check_timeout(host, port, self.timeout))
        return await asyncio.gather(*tasks)
