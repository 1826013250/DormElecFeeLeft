import os
import sys
import platform
import winshell
from win32com.client import Dispatch

from util import get_program_path


def set_autostart(app_name, enable):
    sys_name = platform.system()
    if sys_name == "Windows":
        win_set_autostart(app_name, enable)

def win_set_autostart(app_name, enable):
    app_path = get_program_path()
    startup_path = winshell.startup()
    shortcut_path = os.path.join(startup_path, f"{app_name}.lnk")
    if enable:
        if not os.path.exists(shortcut_path):
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.IconLocation = app_path
            shortcut.save()
    else:
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)