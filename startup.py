import os
import sys
import platform
import subprocess
import traceback

if platform.system() == "Windows":
    import winshell  # noqa
    from win32com.client import Dispatch  # noqa

from util import get_program_path, log_error, log_warning


def set_autostart(app_name: str, enable: bool) -> bool:
    sys_name = platform.system()
    if sys_name == "Windows":
        return win_set_autostart(app_name, enable)
    elif sys_name == "Darwin":
        return macos_set_autostart(app_name, enable)
    elif sys_name == "Linux":
        log_warning("当前不支持Linux开机自启！")
        return False
    log_warning("未知系统环境")
    return False


def win_set_autostart(app_name: str, enable: bool) -> bool:
    app_path = get_program_path()
    startup_path = winshell.startup()
    shortcut_path = os.path.join(startup_path, f"{app_name}.lnk")
    try:
        if enable:
            if not os.path.exists(shortcut_path):
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = app_path
                shortcut.WorkingDirectory = os.path.dirname(app_path)
                shortcut.IconLocation = app_path
                shortcut.save()
                return True
        else:
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                return True
    except Exception as e:
        log_error(traceback.format_exc())
    return False


def macos_set_autostart(app_name: str, enable: bool):
    app_path = get_program_path()
    if ".app/Contents/MacOS/" in app_path:
        app_path = app_path.split(".app/Contents/MacOS/")[0] + ".app"
    if enable:
        script = f'''
            tell application "System Events"
                if not (exists (some login item whose path is "{app_path}")) then
                    make login item at end with properties {{path:"{app_path}", name:"{app_name}", hidden:false}}
                end if
            end tell
            '''
        try:
            subprocess.run(["osascript", "-e", script], check=True)
        except subprocess.CalledProcessError:
            log_error(traceback.format_exc())
            return False
        return True
    else:
        script = f'''
            tell application "System Events"
                delete (every login item whose path is "{app_path}")
            end tell
            '''
        try:
            subprocess.run(["osascript", "-e", script], check=True)
        except subprocess.CalledProcessError:
            log_error(traceback.format_exc())
            return False
        return True
