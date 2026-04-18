# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_time_interval.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QHBoxLayout, QLabel,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_DialogSetTimeInterval(object):
    def setupUi(self, DialogSetTimeInterval):
        if not DialogSetTimeInterval.objectName():
            DialogSetTimeInterval.setObjectName(u"DialogSetTimeInterval")
        DialogSetTimeInterval.resize(226, 96)
        self.verticalLayout = QVBoxLayout(DialogSetTimeInterval)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DialogSetTimeInterval)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinbox_value = QDoubleSpinBox(DialogSetTimeInterval)
        self.spinbox_value.setObjectName(u"spinbox_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinbox_value.sizePolicy().hasHeightForWidth())
        self.spinbox_value.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.spinbox_value)

        self.combo_unit = QComboBox(DialogSetTimeInterval)
        self.combo_unit.setObjectName(u"combo_unit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.combo_unit.sizePolicy().hasHeightForWidth())
        self.combo_unit.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.combo_unit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(DialogSetTimeInterval)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DialogSetTimeInterval)
        self.buttonBox.accepted.connect(DialogSetTimeInterval.accept)
        self.buttonBox.rejected.connect(DialogSetTimeInterval.reject)

        QMetaObject.connectSlotsByName(DialogSetTimeInterval)
    # setupUi

    def retranslateUi(self, DialogSetTimeInterval):
        DialogSetTimeInterval.setWindowTitle(QCoreApplication.translate("DialogSetTimeInterval", u"\u8bbe\u7f6e\u65f6\u95f4\u95f4\u9694", None))
        self.label.setText(QCoreApplication.translate("DialogSetTimeInterval", u"\u8bf7\u8bbe\u7f6e\u65f6\u95f4\u95f4\u9694", None))
    # retranslateUi

