=====
Usage
=====

In order to use FastPortScanner read the following snippet

Follow the example to get list of hosts::

    import asyncio
    from asyncio_fast_portscanner.asyncio_fast_portscanner import FastPortScanner
    loop = asyncio.get_event_loop() # Get event loop, when you are already
                                    # in async function you can await awaitables
                                    # instead of run_until_complete

    scanner = FastPortScanner(timeout, verbose) # timeout is
                                                # max time of task to execute
    result = loop.run_until_complete(scanner.loadHostListByCidr(range))
    # Loading host list by CIDR accepts hosts in format 192.168.1.0/24
    result = loop.run_until_complete(scanner.loadHostListByRange(range))
    # Loads port ranges - for example 192.168.2.1-255
    if not result[0]:
        print(result[1])
        sys.exit(1)
    # Loading hosts return tuple of bool, str - result and reason if False

    result = loop.run_until_complete(scanner.loadPortList(ports))
    # Accepts collection of ints - like 22, 8080
    if not result[0]:
        print(result[1])
        sys.exit(1)

    results = loop.run_until_complete(scanner.gatherResults())
    # In results you will have dicts of "host", "port", "status"
