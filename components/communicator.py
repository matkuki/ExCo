"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import json
import time
import queue
import socket
import functools
import traceback
import multiprocessing
import multiprocessing.connection
from typing import *

import qt
import data
import functions
import components.processcontroller


DEBUG_MODE = False
STATUS_MODE = False


"""
IPC-based communicator
"""
ADDRESS = "localhost"
PORT = 19991
PASSWORD = "ExCo"


def debug_echo(obj: Any, *messages: Any) -> None:
    if DEBUG_MODE:
        print(
            "[{}-{}]".format(obj.__class__.__name__, obj.name),
            " ".join([str(x) for x in messages]),
        )


def status_echo(obj: Any, *messages: Any) -> None:
    if STATUS_MODE:
        print(
            "[{}-{}]".format(obj.__class__.__name__, obj.name),
            " ".join([str(x) for x in messages]),
        )


class CommClient:
    connection: Any = None
    # Callbacks
    receive_callback: Any = None

    def __init__(self, name: str, receive_callback: Any) -> None:
        self.running = False
        self.name = name
        self.receive_callback = receive_callback
        functions.create_thread(self.reinitialize)

    def __del__(self) -> None:
        self.running = False
        if self.connection is not None:
            self.connection.close()

    def reinitialize(self) -> None:
        initialized = False
        while initialized == False:
            try:
                self.connection = multiprocessing.connection.Client(
                    (ADDRESS, PORT), authkey=PASSWORD.encode("utf-8")
                )
                functions.create_thread(self.recv_loop)
                initialized = True
            except KeyboardInterrupt as ke:
                raise ke
            except Exception as ex:
                debug_echo(self, "init error, trying again ...")

    def recv_loop(self) -> None:
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

    def send(self, message: Any) -> None:
        self.connection.send(message)


class CommListener:
    running: bool = False
    stored_connections: list[tuple[Any, Any]] = []
    connection: Any = None
    # Callbacks
    stopped_callback: Any = None

    def __init__(self, name: str, stopped_callback: Any) -> None:
        self.running = False
        self.name = name
        self.stored_connections = []
        self.connection = None
        self.stopped_callback = stopped_callback
        functions.create_thread(self.connecting_loop)

    def __del__(self) -> None:
        self.running = False
        if self.connection is not None:
            self.connection.close()
        for c in self.stored_connections:
            c[0].close()

    def connecting_loop(self) -> None:
        try:
            with multiprocessing.connection.Listener(
                (ADDRESS, PORT), authkey=PASSWORD.encode("utf-8")
            ) as listener:
                debug_echo(self, "Listening ...")
                self.running = True
                while self.running == True:
                    try:
                        conn = listener.accept()
                        self._create_listening_thread(conn, listener.last_accepted)
                    except socket.timeout:
                        pass
        except Exception as ex:
            debug_echo(self, ex)
            self.running = False
            time.sleep(0.1)
            self.stopped_callback()

    def _create_listening_thread(self, connection: Any, last_accepted: Any) -> None:
        self.stored_connections.append((connection, last_accepted))
        functions.create_thread(self._listen, connection, last_accepted)

    def _listen(self, conn: Any, last_accepted: Any) -> None:
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
            debug_echo(self, f"Connection '{last_accepted[1]}' broken!")
            self.stored_connections.remove((conn, last_accepted))
        status_echo(self, "END")

    def send(self, message: Any) -> None:
        for co, info in self.stored_connections:
            co.send(message)

    def close_connections(self) -> None:
        for co, info in self.stored_connections:
            co.close()


class IpcCommunicator(qt.QObject):
    """
    Object for passing messages between processes/applications
    """

    # Signals
    received: qt.pyqtSignal = qt.pyqtSignal(object)

    # Attributes
    name: str | None = None
    client: CommClient | None = None
    listener: CommListener | None = None
    comm_thread: qt.QThread | None = None

    def __init__(self, name: str) -> None:
        super().__init__()

        self.comm_thread = qt.QThread()
        self.moveToThread(self.comm_thread)
        # Connect the startup function of communicator
        self.comm_thread.started.connect(functools.partial(self.initialize, name))
        # Start the process
        self.comm_thread.start()

    def __del__(self) -> None:
        assert self.comm_thread is not None
        self.comm_thread.exit()
        del self.client
        del self.listener

    def initialize(self, name: str) -> None:
        self.name = name
        self.client = CommClient(self.name, self.receive)
        self.listener = CommListener(self.name, self.listener_stopped)

    def listener_stopped(self) -> None:
        assert self.name is not None
        self.listener = CommListener(self.name, self.listener_stopped)

    def receive(self, message: Any) -> None:
        self.received.emit(message)

    def send_to_server(self, message: Any) -> None:
        assert self.client is not None
        self.client.send((self.name, message))

    def multisend(self, message: Any) -> None:
        assert self.listener is not None
        self.listener.send((self.name, message))

    @qt.pyqtSlot(object)
    def send(self, message: Any) -> None:
        assert self.listener is not None
        if self.listener.running == True:
            self.multisend(message)
        else:
            self.send_to_server(message)


"""
File-based communicator
"""


class FileCommunicator(qt.QObject):
    """
    Object for communicating between processes using files
    """

    # Signals
    received: qt.pyqtSignal = qt.pyqtSignal(object)
    __process_directory_queue: qt.pyqtSignal = qt.pyqtSignal()

    # Attributes
    __name: str = ""
    __comm_file_path: str = ""
    __file_watcher: qt.QFileSystemWatcher | None = None
    __processing_lock: Any = multiprocessing.Lock()
    __processing_queue: Any = multiprocessing.Queue()

    def __init__(self, name: str) -> None:
        super().__init__()

        self.__name = name
        self.__comm_file_path = components.processcontroller.inbox_path(os.getpid())

        file_watcher = qt.QFileSystemWatcher(self)
        file_watcher.directoryChanged.connect(self.__directory_changed)
        file_watcher.fileChanged.connect(self.__file_changed)
        file_watcher.addPath(data.settings_directory)
        self.__file_watcher = file_watcher

        self.__process_directory_queue.connect(self.__process_change)

    def __directory_changed(self, path: str) -> None:
        self.__processing_queue.put(path)
        self.__process_directory_queue.emit()

    def __file_changed(self, path: str) -> None:
        self.__processing_queue.put(path)
        self.__process_directory_queue.emit()

    def __process_change(self) -> None:
        acquired = self.__processing_lock.acquire(block=False)
        if not acquired:
            return

        try:
            while True:
                path = self.__processing_queue.get_nowait()
                if os.path.isfile(self.__comm_file_path):
                    with open(self.__comm_file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        _data = json.loads(text)
                        self.received.emit(("FileCommunicator", _data))
                    os.remove(self.__comm_file_path)
        except queue.Empty:
            pass
        except:
            traceback.print_exc()
        finally:
            self.__processing_lock.release()
