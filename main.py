import sys
from datetime import datetime

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QWidget, QMenu, QInputDialog
from PySide6.QtCore import QTimer, QThreadPool
from PySide6.QtGui import QIcon, QAction

from startup import set_autostart
from util import get_power, TimeUnits, Settings, RunnableGetPowerInfo, log_info
from widgets import DialogSetTimeInterval, DialogSelectDormitory

APP_NAME = "DormElecFeeLeft"


class App(QWidget):
    def __init__(self, settings: Settings):
        super().__init__()
        # var
        self.quantity = 0.0
        self.quantity_unit = "NULL"
        self.settings = settings
        self.thread_pool = QThreadPool()

        # init
        self.__init_tray_icon()

        # misc
        self.timer_query = QTimer(self)
        self.timer_query.setInterval(self.__get_query_interval())
        self.timer_query.timeout.connect(self.__query_data)
        QTimer.singleShot(10, self, self._startup)

    def _startup(self):
        if not self.settings.student_id:
            QMessageBox.warning(self, "注意！", "您未配置学号！\n请按下确定在接下来的窗口中输入学号以进行宿舍查询。")
            value, success = QInputDialog.getText(self, "请输入学号", "请输入学号，按取消键退出程序")
            if not success:
                QApplication.instance().quit()
                return
            self.settings.student_id = value
            self.settings.save()
        if not self.settings.last_dorm_id:
            btn = QMessageBox.warning(self, "注意！", "您没有选择宿舍，是否立即选择？",
                                      buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if btn == QMessageBox.StandardButton.Ok:
                self.__select_dormitory()
        else:
            self.action_text_dormitory.setText(self.settings.last_dorm_name)
            self.timer_query.start()
            self.__query_data()

    def __init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.DialogQuestion))
        self.tray_menu = QMenu()
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_menu.aboutToShow.connect(self.__update_tray_texts)

        # Actions
        self.action_text_dormitory = QAction("您未选择宿舍", self)
        self.action_text_dormitory.setEnabled(False)
        self.tray_menu.addAction(self.action_text_dormitory)

        self.action_text_details = QAction("剩余电量：-- 度", self)
        self.action_text_details.setEnabled(False)
        self.tray_menu.addAction(self.action_text_details)

        self.tray_menu.addSeparator()

        action_modify_student_id = QAction("设置学号", self)
        action_modify_student_id.triggered.connect(self.__modify_student_id)
        self.tray_menu.addAction(action_modify_student_id)

        action_select_dormitory = QAction("选择宿舍", self)
        action_select_dormitory.triggered.connect(self.__select_dormitory)
        self.tray_menu.addAction(action_select_dormitory)

        action_set_warn_limit = QAction("设置警告下限", self)
        action_set_warn_limit.triggered.connect(self.__modify_warn_limit)
        self.tray_menu.addAction(action_set_warn_limit)

        action_set_query_interval = QAction("设置查询间隔", self)
        action_set_query_interval.triggered.connect(self.__modify_query_interval)
        self.tray_menu.addAction(action_set_query_interval)

        action_toggle_startup_on_login = QAction("开机自启", self)
        action_toggle_startup_on_login.setCheckable(True)
        action_toggle_startup_on_login.setChecked(self.settings.startup_on_login)
        action_toggle_startup_on_login.triggered.connect(self.__set_startup_on_login)
        self.__set_startup_on_login(self.settings.startup_on_login)
        self.tray_menu.addAction(action_toggle_startup_on_login)

        self.tray_menu.addSeparator()
        action_exit = QAction("退出", self)
        action_exit.triggered.connect(lambda: QApplication.instance().quit())
        self.tray_menu.addAction(action_exit)

        self.tray_icon.show()

    def __update_tray_texts(self):
        self.action_text_details.setText(f"剩余电量：{self.quantity:.2f} {self.quantity_unit}")

    def __select_dormitory(self):
        dialog = DialogSelectDormitory(self.settings.student_id, self)
        if dialog.exec():
            self.settings.last_dorm_id = dialog.selected_dorm_id
            self.settings.last_dorm_name = dialog.selected_dorm_name
            self.action_text_dormitory.setText(self.settings.last_dorm_name)
            self.timer_query.start()
            self.__query_data()
            self.settings.save()

    def __set_startup_on_login(self, status: bool):
        if set_autostart(APP_NAME, status):
            self.settings.startup_on_login = status
            self.settings.save()
        else:
            QMessageBox.warning(self, "警告", "添加/删除开机自启项目失败！\n"
                                "可能是当前系统不支持或出现错误！\n"
                                "查看日志以查询具体消息")

    def __modify_student_id(self):
        value, success = QInputDialog.getText(self, "设置学号", "请输入学号")
        if success:
            self.settings.student_id = value
            self.settings.save()

    def __modify_warn_limit(self):
        value, success = QInputDialog.getDouble(self, "请输入数据", "请输入警告下限阈值（单位：度）",
                                                value=self.settings.warn_limit,
                                                minValue=0)
        if success:
            self.settings.warn_limit = value
            self.__query_data()
            self.settings.save()

    def __modify_query_interval(self):
        r = DialogSetTimeInterval.get_value(self.settings.query_interval, self.settings.query_interval_unit)
        if r:
            self.settings.query_interval, self.settings.query_interval_unit = r
            self.timer_query.setInterval(self.__get_query_interval())
            self.__query_data()
            self.settings.save()

    def __get_query_interval(self):
        return int({
            TimeUnits.MILLISECONDS: self.settings.query_interval,
            TimeUnits.SECONDS: self.settings.query_interval * 1000,
            TimeUnits.MINUTES: self.settings.query_interval * 60 * 1000,
            TimeUnits.HOURS: self.settings.query_interval * 60 * 60 * 1000,
            TimeUnits.DAYS: self.settings.query_interval * 24 * 60 * 60 * 1000,
        }[self.settings.query_interval_unit])

    def __query_data(self):
        if not self.settings.last_dorm_id:
            QMessageBox.warning(self, "注意！", "您未选择宿舍！请前往菜单选择您的宿舍")
            self.timer_query.stop()
            return
        log_info("查询开始!")
        runnable = RunnableGetPowerInfo(self.settings.last_dorm_id)
        runnable.signal.signal_power_request_finished.connect(self.__query_data_callback)
        self.thread_pool.start(runnable)

    def __query_data_callback(self, quantity, quantity_unit):
        if quantity > 0:
            self.quantity = quantity
            self.quantity_unit = quantity_unit
            if self.quantity <= self.settings.warn_limit:
                self.timer_query.stop()
                QMessageBox.warning(self,"DormElecFeeLeft: 警告",
                                    "当前电量已到达警告阈值！\n"
                                    + f"当前：{self.quantity} 度, 警告阈值：{self.settings.warn_limit} 度\n"
                                    + "请及时缴费！")
                self.timer_query.start()
        else:
            self.timer_query.stop()
            QMessageBox.critical(self, "DormElecFeeLeft: 错误",
                                 "获取电力信息出错，原因:\n"
                                 + quantity_unit + "\n"
                                 + "请检查网络后按确定重试。")
            self.timer_query.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = App(Settings.load())
    sys.exit(app.exec())