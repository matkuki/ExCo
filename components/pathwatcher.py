"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import os
import threading
from enum import Enum, auto
from threading import Lock, Timer
from types import TracebackType
from typing import Any, Dict, List, Optional, Set

import qt
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class FileEvent(Enum):
    """
    Enumeration of all possible file system events.
    """

    MODIFIED = auto()
    CREATED = auto()
    DELETED = auto()
    MOVED = auto()
    RENAME = auto()


class PathWatcher(qt.QObject):
    """
    A class to monitor file system changes for specific files using watchdog.
    Files can be dynamically added and removed from monitoring.
    """

    # Define a custom signal that matches the callback's signature
    file_changed = qt.pyqtSignal(object, str, object, object)

    ECHO_ENABLED: bool = True  # Class variable to control echo output

    def __init__(self, parent: Optional[qt.QObject] = None) -> None:
        """
        Initialize the PathWatcher.
        """
        super().__init__(parent)
        self.monitored_files: List[str] = []  # List of files being monitored
        self.observers: Dict[
            str, Observer
        ] = {}  # Dictionary mapping directory paths to observers
        self._lock: threading.Lock = (
            threading.Lock()
        )  # Thread safety for file list operations

    def echo(self, message: str) -> None:
        """Print a message only if ECHO_ENABLED is True."""
        if self.ECHO_ENABLED:
            print(message)

    def add_file(self, file_path: str) -> bool:
        """
        Add a file to the monitoring list.

        Args:
            file_path: Path to the file to monitor

        Returns:
            True if file was added successfully, False otherwise
        """
        file_path = os.path.abspath(file_path)

        with self._lock:
            if file_path in self.monitored_files:
                self.echo(f"File {file_path} is already being monitored")
                return False

            if not os.path.exists(file_path):
                self.echo(f"Warning: File {file_path} does not exist")

            self.monitored_files.append(file_path)

            # Get the directory containing this file
            directory: str = os.path.dirname(file_path)

            # If we're not already watching this directory, start watching it
            if directory not in self.observers:
                self._start_watching_directory(directory)

            self.echo(f"Added {file_path} to monitoring list")
            return True

    def remove_file(self, file_path: str) -> bool:
        """
        Remove a file from the monitoring list.

        Args:
            file_path: Path to the file to stop monitoring

        Returns:
            True if file was removed successfully, False otherwise
        """
        file_path = os.path.abspath(file_path)

        with self._lock:
            if file_path not in self.monitored_files:
                self.echo(f"File {file_path} is not being monitored")
                return False

            self.monitored_files.remove(file_path)

            # Check if we still need to watch the directory
            directory: str = os.path.dirname(file_path)
            still_needed: bool = any(
                os.path.dirname(f) == directory for f in self.monitored_files
            )

            if not still_needed and directory in self.observers:
                self._stop_watching_directory(directory)

            self.echo(f"Removed {file_path} from monitoring list")
            return True

    def get_monitored_files(self) -> List[str]:
        """
        Get a copy of the list of monitored files.

        Returns:
            Copy of the monitored files list
        """
        with self._lock:
            return self.monitored_files.copy()

    def clear_all_files(self) -> None:
        """Remove all files from monitoring and stop all observers."""
        with self._lock:
            self.monitored_files.clear()
            for directory in list(self.observers.keys()):
                self._stop_watching_directory(directory)
            self.echo("Cleared all monitored files")

    def add_files_batch(self, file_paths: List[str]) -> int:
        """
        Add multiple files efficiently in one operation.

        Args:
            file_paths: List of file paths to monitor

        Returns:
            Number of files successfully added
        """
        directories_to_watch: Set[str] = set()
        added_count: int = 0

        with self._lock:
            for file_path in file_paths:
                file_path = os.path.abspath(file_path)
                if file_path not in self.monitored_files:
                    if not os.path.exists(file_path):
                        self.echo(f"Warning: File {file_path} does not exist")

                    self.monitored_files.append(file_path)
                    directories_to_watch.add(os.path.dirname(file_path))
                    added_count += 1
                else:
                    self.echo(f"File {file_path} is already being monitored")

        # Start watching all new directories at once
        for directory in directories_to_watch:
            if directory not in self.observers:
                self._start_watching_directory(directory)

        print(f"Added {added_count} files to monitoring list")
        return added_count

    def _start_watching_directory(self, directory: str) -> None:
        """Start watching a directory with a new observer."""
        handler: FileChangeHandler = FileChangeHandler(self)
        observer: Observer = Observer()
        observer.schedule(handler, directory, recursive=False)
        observer.start()

        self.observers[directory] = observer
        self.echo(f"Started watching directory: {directory}")

    def _stop_watching_directory(self, directory: str) -> None:
        """Stop watching a directory and clean up the observer."""
        if directory in self.observers:
            observer: Observer = self.observers[directory]
            observer.stop()
            observer.join()
            del self.observers[directory]
            self.echo(f"Stopped watching directory: {directory}")

    def _handle_file_event(
        self,
        event_type: FileEvent,
        source_path: str,
        destination_path: Optional[str],
        modification_time: Optional[float],
    ) -> None:
        """
        Handle a file system event for one of our monitored files.

        Args:
            event_type: Type of event (FileEvent enum value)
            source_path: Source path of the file
            destination_path: Destination path (only for MOVED events)
        """
        if destination_path:
            self.echo(f"File {event_type.name}: {source_path} -> {destination_path}")
        else:
            self.echo(f"File {event_type.name}: {source_path}")

        # Call the callback if provided
        self.file_changed.emit(
            event_type, source_path, destination_path, modification_time
        )

    def start_monitoring(self) -> None:
        """Start the monitoring process. This is non-blocking."""
        self.echo(f"Started monitoring {len(self.monitored_files)} files")

    def stop_monitoring(self) -> None:
        """Stop all monitoring and clean up resources."""
        with self._lock:
            for directory in list(self.observers.keys()):
                self._stop_watching_directory(directory)
            self.echo("Stopped all monitoring")

    def get_observer_count(self) -> int:
        """
        Get the number of active directory observers.

        Returns:
            Number of active observers
        """
        with self._lock:
            return len(self.observers)

    def update_file_path(self, old_path: str, new_path: str) -> bool:
        """
        Update a monitored file path (useful for external move operations).

        Args:
            old_path: Current path being monitored
            new_path: New path to monitor instead

        Returns:
            True if update was successful, False otherwise
        """
        old_path = os.path.abspath(old_path)
        new_path = os.path.abspath(new_path)

        with self._lock:
            if old_path not in self.monitored_files:
                self.echo(f"File {old_path} is not being monitored")
                return False

            if new_path in self.monitored_files:
                self.echo(f"File {new_path} is already being monitored")
                return False

            # Remove old path and add new path
            self.monitored_files.remove(old_path)
            self.monitored_files.append(new_path)

            # Handle directory observer management
            old_directory = os.path.dirname(old_path)
            new_directory = os.path.dirname(new_path)

            # Check if we still need to watch the old directory
            still_needed_old = any(
                os.path.dirname(f) == old_directory for f in self.monitored_files
            )
            if not still_needed_old and old_directory in self.observers:
                self._stop_watching_directory(old_directory)

            # Start watching the new directory if not already watching
            if new_directory not in self.observers:
                self._start_watching_directory(new_directory)

            self.echo(f"Updated file path: {old_path} -> {new_path}")
            return True

    def __enter__(self) -> "PathWatcher":
        """Context manager entry."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Context manager exit - clean up resources."""
        self.stop_monitoring()


class FileChangeHandler(FileSystemEventHandler):
    """Event handler for watchdog that filters events to only monitored files."""

    def __init__(self, path_watcher: PathWatcher) -> None:
        self.path_watcher: PathWatcher = path_watcher
        super().__init__()
        # A dictionary to store a threading.Timer and last event type for each file.
        self._debounce_timers: Dict[str, Dict[str, Any]] = {}
        # A debounce interval in seconds.
        self._debounce_interval: float = 0.5
        # A lock to ensure thread-safe access to the _debounce_timers dictionary.
        self._timer_lock: Lock = Lock()

    def _start_debounce_timer(self, file_path: str, event_type: "FileEvent") -> None:
        """
        Starts or resets a threading.Timer for a specific file and event type.
        """
        file_path_abs: str = os.path.abspath(file_path)

        is_monitored: bool = False
        with self.path_watcher._lock:
            if file_path_abs in self.path_watcher.monitored_files:
                is_monitored = True

        if not is_monitored:
            return

        with self._timer_lock:
            timer_data: Optional[Dict[str, Any]] = self._debounce_timers.get(
                file_path_abs
            )

            if timer_data and timer_data["type"] == event_type:
                timer_data["timer"].cancel()

            timer: Timer = Timer(
                self._debounce_interval,
                self._handle_timer_timeout,
                args=[file_path_abs, event_type],
            )
            self._debounce_timers[file_path_abs] = {
                "timer": timer,
                "type": event_type,
            }
            timer.start()

    def _handle_timer_timeout(self, file_path: str, event_type: FileEvent) -> None:
        """
        This function is called when the debounce timer for a file expires.
        It retrieves the mtime and passes it to the handler.
        """
        if event_type == FileEvent.DELETED:
            # Check if file still doesn't exist
            if not os.path.exists(file_path):
                with self.path_watcher._lock:
                    if file_path in self.path_watcher.monitored_files:
                        self.path_watcher.monitored_files.remove(file_path)
                self.path_watcher._handle_file_event(
                    FileEvent.DELETED, file_path, None, None
                )
                self.path_watcher.echo(f"File deleted: {file_path}")
            else:
                # File was recreated, treat as modified
                mtime = os.path.getmtime(file_path)
                self.path_watcher._handle_file_event(
                    FileEvent.MODIFIED, file_path, None, mtime
                )
                self.path_watcher.echo(
                    f"File reappeared, treated as MODIFIED: {file_path}"
                )
            return

        mtime: Optional[float] = None
        try:
            mtime = os.path.getmtime(file_path)
        except FileNotFoundError:
            self.path_watcher.echo(f"File not found for mtime check: {file_path}")
            return

        self.path_watcher._handle_file_event(event_type, file_path, None, mtime)
        self.path_watcher.echo(
            f"Handled debounced event: {event_type.name} on {file_path} with mtime {mtime}"
        )

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._start_debounce_timer(event.src_path, FileEvent.MODIFIED)

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._start_debounce_timer(event.src_path, FileEvent.CREATED)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._start_debounce_timer(event.src_path, FileEvent.DELETED)

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory and hasattr(event, "dest_path"):
            source_path: str = os.path.abspath(event.src_path)
            destination_path: str = os.path.abspath(event.dest_path)

            source_dir = os.path.dirname(source_path)
            destination_dir = os.path.dirname(destination_path)

            event_to_emit: FileEvent
            if source_dir == destination_dir:
                event_to_emit = FileEvent.RENAME
            else:
                event_to_emit = FileEvent.MOVED

            with self.path_watcher._lock:
                if source_path in self.path_watcher.monitored_files:
                    self.path_watcher.monitored_files.remove(source_path)

                    if event_to_emit == FileEvent.RENAME:
                        self.path_watcher.monitored_files.append(destination_path)

                    with self._timer_lock:
                        if source_path in self._debounce_timers:
                            timer_data = self._debounce_timers.pop(source_path)
                            timer_data["timer"].cancel()
                            if event_to_emit == FileEvent.RENAME:
                                self._debounce_timers[destination_path] = timer_data

                    self.path_watcher._handle_file_event(
                        event_to_emit,
                        source_path,
                        destination_path,
                        None,
                    )

                    if event_to_emit == FileEvent.RENAME:
                        self.path_watcher.echo(
                            f"Monitored file RENAME: {source_path} -> {destination_path}"
                        )
                    else:
                        self.path_watcher.echo(
                            f"Stopped monitoring: {source_path} (moved to {destination_path})"
                        )
