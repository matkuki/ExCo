# -*- coding: utf-8 -*-

"""
Copyright (c) 2013-2023 Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import time
import socket
import functools
import multiprocessing
import multiprocessing.connection
from typing import *

import data
import functions


DEBUG_MODE = False
STATUS_MODE = False

ADDRESS = 'localhost'
PORT = 19991
PASSWORD = "ExCo"

def debug_echo(obj, *messages):
    if DEBUG_MODE:
        print(
            "[{}-{}]".format(obj.__class__.__name__, obj.name),
            " ".join([str(x) for x in messages])
        )

def status_echo(obj, *messages):
    if STATUS_MODE:
        print(
            "[{}-{}]".format(obj.__class__.__name__, obj.name),
            " ".join([str(x) for x in messages])
        )

class CommClient:
    connection = None
    # Callbacks
    receive_callback = None

    def __init__(self, name, receive_callback):
        self.running = False
        self.name = name
        self.receive_callback = receive_callback
        functions.create_thread(self.reinitialize)

    def __del__(self):
        self.running = False
        if self.connection is not None:
            self.connection.close()

    def reinitialize(self):
        initialized = False
        while initialized == False:
            try:
                self.connection = multiprocessing.connection.Client(
                    (ADDRESS, PORT),
                    authkey=PASSWORD.encode('utf-8')
                )
                functions.create_thread(self.recv_loop)
                initialized = True
            except KeyboardInterrupt as ke:
                raise ke
            except Exception as ex:
                debug_echo(self, "init error, trying again ...")

    def recv_loop(self):
        try:
            debug_echo(self, "[CommClient] Receiving ...")
            self.running = True
            while self.running == True:
                if self.connection.poll():
                    status_echo(self, "recv")
                    _data = self.connection.recv()
                    status_echo(self, "recv success")
                    debug_echo(self, "Received:\n{}".format(_data))
                    self.receive_callback(_data)
                else:
                    time.sleep(0.1)
        except Exception as ex:
            debug_echo(self, "recv loop error:\n{}".format(str(ex)))
            self.reinitialize()

    def send(self, message):
        self.connection.send(message)


class CommListener:
    running = False
    stored_connections = None
    connection = None
    # Callbacks
    stopped_callback = None

    def __init__(self, name, stopped_callback):
        self.running = False
        self.name = name
        self.stored_connections = []
        self.connection = None
        self.stopped_callback = stopped_callback
        functions.create_thread(self.connecting_loop)

    def __del__(self):
        self.running = False
        if self.connection is not None:
            self.connection.close()
        for c in self.stored_connections:
            c[0].close()

    def connecting_loop(self):
        try:
            with multiprocessing.connection.Listener(
                (ADDRESS, PORT),
                authkey=PASSWORD.encode('utf-8')) as listener:
                    debug_echo(self, "Listening ...")
                    self.running = True
#                    listener._listener._socket.settimeout(1.0)
                    while self.running == True:
                        try:
                            conn = listener.accept()
                            self._create_listening_thread(
                                conn, listener.last_accepted
                            )
                        except socket.timeout:
                            pass
        except Exception as ex:
#            debug_echo(self, ex)
            self.running = False
            time.sleep(0.1)
            self.stopped_callback()

    def _create_listening_thread(self, connection, last_accepted):
        self.stored_connections.append((connection, last_accepted))
        functions.create_thread(self._listen, connection, last_accepted)

    def _listen(self, conn, last_accepted):
        status_echo(self, "START")
        try:
            while self.running:
                status_echo(self, "listen")
                self.connection = conn
                _data = conn.recv()
                self.connection = None
                status_echo(self, "listen success")
#                debug_echo(self, "received data:", _data)
                # Resend to all connections
                self.send(_data)
        except:
            self.connection = None
            status_echo(self, "listen error")
            debug_echo(
                self, f"Connection '{last_accepted[1]}' broken!"
            )
            self.stored_connections.remove((conn, last_accepted))
        status_echo(self, "END")

    def send(self, message):
        for co, info in self.stored_connections:
            co.send(message)

    def close_connections(self):
        for co, info in self.stored_connections:
            co.close()


class Communicator(data.QObject):
    """
    Object for passing messages between processes/applications
    """
    # Signals
    received: data.pyqtSignal = data.pyqtSignal(object)
    # Attributes
    name = None
    client = None
    listener = None
    comm_thread = None

    def __init__(self, name):
        super().__init__()

        self.comm_thread = data.QThread()
        self.moveToThread(self.comm_thread)
        # Connect the startup function of communicator
        self.comm_thread.started.connect(
            functools.partial(self.initialize, name)
        )
        # Start the process
        self.comm_thread.start()

    def __del__(self):
        self.comm_thread.exit()
        del self.client
        del self.listener

    def initialize(self, name):
        self.name = name
        self.client = CommClient(self.name, self.receive)
        self.listener = CommListener(self.name, self.listener_stopped)

    def listener_stopped(self):
        self.listener = CommListener(self.name, self.listener_stopped)

    def receive(self, message):
        self.received.emit(message)

    def send_to_server(self, message):
        self.client.send((self.name, message))

    def multisend(self, message):
        self.listener.send((self.name, message))

    @data.pyqtSlot(object)
    def send(self, message):
        if self.listener.running == True:
            self.multisend(message)
        else:
            self.send_to_server(message)
