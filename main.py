#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-02-02
# Copyright © 2024 Davidson Engineering Ltd.
# ---------------------------------------------------------------------------
"""network_simple - A simple network client and server for sending and receiving data."""
# ---------------------------------------------------------------------------


import time
import threading
import logging
import random
import time
from collections import deque


logging.basicConfig(level=logging.DEBUG)

from network_simple.client import SimpleClientTCP
from network_simple.server import SimpleServerTCP


def client_tcp():

    client_config = {
        "host": "localhost",
        "port": 9000,
    }
    client = SimpleClientTCP(**client_config)
    random_metrics = [("cpu_usage", random.random(), time.time()) for _ in range(4095)]
    for metric in random_metrics:
        client.add_to_queue(metric)
    client.send()
    while True:
        time.sleep(1)


def server_tcp():
    buffer = deque()
    server = SimpleServerTCP(
        output_buffer=buffer,
        host="localhost",
        port=9000,
        autostart=True,
    )
    print(server)
    while True:
        print(f"{len(buffer)=}")
        print(f"{server.request_queue_size=}")
        time.sleep(1)


from network_simple.client import SimpleClientUDP
from network_simple.server import SimpleServerUDP

from buffered.buffer import PackagedBuffer


def client_udp():

    client_config = {
        "host": "localhost",
        "port": 9000,
    }
    client = SimpleClientUDP(**client_config)
    random_metrics = [("cpu_usage", random.random(), time.time()) for _ in range(4095)]
    for metric in random_metrics:
        client.add_to_queue(metric)
    client.send()
    while True:
        time.sleep(1)


def server_udp():
    buffer = PackagedBuffer()
    server = SimpleServerUDP(
        output_buffer=buffer,
        host="localhost",
        port=9000,
        autostart=True,
    )
    print(server)
    while True:
        print(len(buffer))
        time.sleep(1)


def run_server_client(server, client):

    server_thread = threading.Thread(target=server)
    server_thread.start()
    time.sleep(1)

    client_thread = threading.Thread(target=client)
    client_thread.start()

    # server_thread.join()
    # client_thread.join()

    while True:
        time.sleep(1)


if __name__ == "__main__":

    # UDP client and server
    run_server_client(server_udp, client_udp)

    # TCP client and server
    # run_server_client(server_tcp, client_tcp)
