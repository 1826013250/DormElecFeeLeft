from typing import Tuple

from PySide6.QtCore import QModelIndex, Qt, QThreadPool, QTimer
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLabel, QAbstractItemView

from design.set_time_interval import Ui_DialogSetTimeInterval
from design.dorm_selection import Ui_DialogDormSelection
from util import TimeUnits, RunnableGetDormInfo


class NormalDialog(QDialog):
    def __init__(self, parent=None, title="Dialog", msg="Message"):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setWindowTitle(title)
        self.text = QLabel(msg)
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.text)

    def closeEvent(self, event, /):
        event.ignore()


class DialogSetTimeInterval(QDialog, Ui_DialogSetTimeInterval):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.combo_unit.addItems((
            TimeUnits.MILLISECONDS.value,
            TimeUnits.SECONDS.value,
            TimeUnits.MINUTES.value,
            TimeUnits.HOURS.value,
            TimeUnits.DAYS.value
        ))

    def __init_values(self):
        if self.parent():
            self.spinbox_value.setValue(self.parent().query_interval)
            self.combo_unit.setCurrentIndex(
                {
                    TimeUnits.MILLISECONDS: 0,
                    TimeUnits.SECONDS: 1,
                    TimeUnits.MINUTES: 2,
                    TimeUnits.HOURS: 3,
                    TimeUnits.DAYS: 4
                }[self.parent().query_interval_unit]
            )

    def exec(self):
        self.__init_values()
        return super().exec()

    @classmethod
    def get_value(cls, initial_value = 0, initial_unit = TimeUnits.MILLISECONDS) -> None | Tuple[float, TimeUnits]:
        dialog = DialogSetTimeInterval()
        dialog.spinbox_value.setValue(initial_value)
        dialog.combo_unit.setCurrentIndex(
            {
                TimeUnits.MILLISECONDS: 0,
                TimeUnits.SECONDS: 1,
                TimeUnits.MINUTES: 2,
                TimeUnits.HOURS: 3,
                TimeUnits.DAYS: 4
            }[initial_unit]
        )
        if dialog.exec():
            return dialog.spinbox_value.value(), TimeUnits(dialog.combo_unit.currentText())
        return None


class DialogSelectDormitory(QDialog, Ui_DialogDormSelection):
    def __init__(self, student_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.student_id = student_id
        self.selected_dorm_id = None
        self.selected_dorm_name = None
        self.thread_pool = QThreadPool()

        self.model = QStandardItemModel()
        self.column_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.column_view.clicked.connect(self.__on_view_clicked)
        self.column_view.setModel(self.model)
        self.__init_first_data()

    def __init_first_data(self):
        self.parent_item = self.model
        self.model.appendRow(QStandardItem("正在加载..."))
        self.dialog = NormalDialog(self, "请稍后", "正在请求数据...")
        runnable = RunnableGetDormInfo(self.student_id, {
                "op_type": 0,
                "area_id": "0",
                "build_id": "0",
                "level_id": "0",
            })
        runnable.signal.signal_dorm_info_request_finished.connect(self.__on_request_finished)
        self.thread_pool.start(runnable)
        self.dialog.exec()

    def __on_view_clicked(self, index: QModelIndex):
        self.parent_item = self.model.itemFromIndex(index)
        if self.parent_item.rowCount() == 0:
            data = self.parent_item.data(Qt.ItemDataRole.UserRole)
            if data["op_type"] == 4:
                self.selected_dorm_id = data["dorm_id"]
                self.selected_dorm_name = self.parent_item.data(Qt.ItemDataRole.UserRole + 1)
                return
            self.selected_dorm_id = None
            self.parent_item.appendRow(QStandardItem("正在加载..."))
            self.dialog = NormalDialog(self, "请稍后", "正在请求数据...")
            runnable = RunnableGetDormInfo(self.student_id, data)
            runnable.signal.signal_dorm_info_request_finished.connect(self.__on_request_finished)
            self.thread_pool.start(runnable)
            self.dialog.exec()

    def __on_request_finished(self, r, data):
        self.dialog.accept()
        if isinstance(r, list) and len(r) == 1:
            QMessageBox.critical(self, "错误！", "获取信息失败！")
            QTimer.singleShot(10, self, self.reject)
            return
        self.parent_item.removeRow(0)
        for i in r:
            item = QStandardItem(i["name"])
            item_data = {
                "op_type": data["op_type"] + 1,
                "area_id": data["area_id"],
                "build_id": data["build_id"],
                "level_id": data["level_id"],
            }
            item_data[str(["area_id", "build_id", "level_id", "dorm_id"][data["op_type"]])] = i["id"]
            item.setData(item_data, Qt.ItemDataRole.UserRole)
            if isinstance(self.parent_item, QStandardItem):
                display_name = self.parent_item.data(Qt.ItemDataRole.UserRole + 1)
                if display_name:
                    item.setData(f"{display_name}→{i['name']}", Qt.ItemDataRole.UserRole + 1)
                else:
                    item.setData(f"{i['name']}", Qt.ItemDataRole.UserRole + 1)
            else:
                item.setData(i["name"], Qt.ItemDataRole.UserRole + 1)
            self.parent_item.appendRow(item)
        self.column_view.setColumnWidths([150 for _ in range(4)])
        self.model.layoutChanged.emit()

    def accept(self, /):
        if not self.selected_dorm_id:
            QMessageBox.warning(self, "注意", "你还没有选择一个宿舍号！")
            return
        super().accept()
