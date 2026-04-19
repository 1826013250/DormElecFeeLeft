import os
import sys
import json
from pathlib import Path
from typing import Tuple
from datetime import datetime
from enum import Enum

from requests import post
from PySide6.QtCore import QRunnable, Signal, QObject

URL = "https://cloudpaygateway.59wanmei.com:8087/paygateway/smallpaygateway/trade"


def get_program_path() -> str:
    if hasattr(sys, "frozen") or "__compiled__" in globals():
        return str(Path(sys.argv[0]).resolve())
    return str(Path(sys.argv[0]).absolute())


def get_program_dir() -> str:
    return os.path.dirname(get_program_path())


def get_power(room_id: str) -> Tuple[float, str]:
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": "samllProgramGetRoomState",
        "bizcontent": json.dumps({"payproid": 726, "schoolcode": "43", "roomverify": room_id, "businesstype": 2}),
        "sourceId": 1
    }
    resp = post(URL, json=data).json()
    if resp["returncode"] == "SUCCESS":
        data = resp["businessData"]
        return float(data["quantity"]), data["quantityunit"]
    return -1, resp["returnmsg"]


def get_details(student_id: str, op_type: int, area_id: str = "0", build_id: str = "0", level_id: str = "0") -> list | dict:
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": "samllProgramGetRoom",
        "bizcontent": json.dumps({
            "payproid": 726,
            "schoolno": "43",
            "businesstype": 2,
            "idserial": student_id,
            "optype": str(op_type),
            "areaid": area_id,
            "buildid": build_id,
            "unitid": "0",
            "levelid": level_id
        }),
        "sourceId": 1
    }
    resp = post(URL, json=data).json()
    if resp["returncode"] == "SUCCESS":
        return resp["businessData"]
    return resp


def log_info(*args, sep=" ", end="\n"):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}/INFO] ", *args, sep=sep, end=end)


def log_error(*args, sep=" ", end="\n"):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}/ERROR] ", *args, sep=sep, end=end)


def log_warning(*args, sep=" ", end="\n"):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}/WARNING] ", *args, sep=sep, end=end)


class TimeUnits(Enum):
    MILLISECONDS = "毫秒"
    SECONDS = "秒"
    MINUTES = "分钟"
    HOURS = "小时"
    DAYS = "天"


class RunnableSignals(QObject):
    signal_dorm_info_request_finished = Signal(object, object)
    signal_power_request_finished = Signal(object, object)


class RunnableGetDormInfo(QRunnable):
    def __init__(self, student_id: str, data: dict):
        super().__init__()
        self.data = data
        self.student_id = student_id
        self.signal = RunnableSignals()

    def run(self):
        r = get_details(self.student_id, self.data["op_type"] + 1, self.data["area_id"], self.data["build_id"], self.data["level_id"])
        self.signal.signal_dorm_info_request_finished.emit(r, self.data)


class RunnableGetPowerInfo(QRunnable):
    def __init__(self, dorm_id: str):
        super().__init__()
        self.dorm_id = dorm_id
        self.signal = RunnableSignals()

    def run(self):
        q, qu = get_power(self.dorm_id)
        self.signal.signal_power_request_finished.emit(q, qu)


class Settings:
    def __init__(self, startup_on_login: bool, query_interval: float, query_interval_unit: TimeUnits,
                 warn_limit: float, student_id: str, last_dorm_id: str, last_dorm_name: str):
        self.startup_on_login = startup_on_login
        self.query_interval = query_interval
        self.query_interval_unit = query_interval_unit
        self.warn_limit = warn_limit
        self.student_id = student_id
        self.last_dorm_id = last_dorm_id
        self.last_dorm_name = last_dorm_name

    @classmethod
    def load(cls):
        settings_path = os.path.join(get_program_dir(), "settings.json")
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                dic = json.load(f)
                return Settings(
                    startup_on_login=dic["startup_on_login"],
                    query_interval=dic["query_interval"],
                    query_interval_unit=TimeUnits(dic["query_interval_unit"]),
                    warn_limit=dic["warn_limit"],
                    student_id=dic["student_id"],
                    last_dorm_id=dic["last_dorm_id"],
                    last_dorm_name=dic["last_dorm_name"]
                )
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, KeyError):
            s = Settings(False, 1.0, TimeUnits.HOURS, 20.0, "", "", "")
            s.save()
            return s

    def save(self):
        settings_path = os.path.join(get_program_dir(), "settings.json")
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump({
                "startup_on_login": self.startup_on_login,
                "query_interval": self.query_interval,
                "query_interval_unit": self.query_interval_unit.value,
                "warn_limit": self.warn_limit,
                "student_id": self.student_id,
                "last_dorm_id": self.last_dorm_id,
                "last_dorm_name": self.last_dorm_name
            }, f, ensure_ascii=False, indent=4)