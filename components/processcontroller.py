"""
Copyright (c) 2013-present Matic Kukovec.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import json
import os
import traceback
from typing import Any

import data
import functions


PID_FILE: str = functions.unixify_join(data.settings_directory, "pid_list.txt")


def is_pid_running(pid: int) -> bool:
    import psutil

    try:
        if not psutil.pid_exists(pid):
            return False

        process = psutil.Process(pid)
        if not process.is_running():
            return False

        name = process.name().lower()
        if "python" in name or "exco":
            return True

        return False
    except Exception:
        return False


def get_running_pids() -> list[int]:
    pids: list[int] = []
    if os.path.isfile(PID_FILE):
        with open(PID_FILE, "r", encoding="utf-8") as f:
            for line in f:
                pid_str = line.strip()
                if pid_str.isdigit():
                    pid = int(pid_str)
                    if is_pid_running(pid):
                        pids.append(pid)
    return sorted(pids)


def inbox_path(pid: int) -> str:
    return functions.unixify_join(data.settings_directory, f"instance_{pid}.json")


def send_to_instance(pid: int, message: dict[str, Any]) -> None:
    path = inbox_path(pid)
    with open(path, "w+", encoding="utf-8", newline="\n") as f:
        json.dump(message, f, indent=4, ensure_ascii=False)


def broadcast(message: dict[str, Any], exclude_self: bool = True) -> list[int]:
    own_pid = os.getpid()
    targets: list[int] = []
    for pid in get_running_pids():
        if exclude_self and pid == own_pid:
            continue
        send_to_instance(pid, message)
        targets.append(pid)
    return targets


def _cleanup_stale_inboxes(live_pids: set[int]) -> None:
    for fname in os.listdir(data.settings_directory):
        if fname.startswith("instance_") and fname.endswith(".json"):
            pid_str = fname[9:-5]
            if pid_str.isdigit() and int(pid_str) not in live_pids:
                try:
                    os.remove(os.path.join(data.settings_directory, fname))
                except OSError:
                    pass


def check_opened_excos() -> int:
    try:
        live_pids = get_running_pids()
        all_pids = [str(os.getpid())] + [str(p) for p in live_pids if p != os.getpid()]

        with open(PID_FILE, "w+", encoding="utf-8") as f:
            f.write("\n".join(all_pids))

        _cleanup_stale_inboxes(set(int(p) for p in all_pids))

        return len(all_pids)
    except:
        return -1
