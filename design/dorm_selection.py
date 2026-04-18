# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dorm_selection.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QColumnView, QDialog,
    QDialogButtonBox, QSizePolicy, QVBoxLayout, QWidget)

class Ui_DialogDormSelection(object):
    def setupUi(self, DialogDormSelection):
        if not DialogDormSelection.objectName():
            DialogDormSelection.setObjectName(u"DialogDormSelection")
        DialogDormSelection.resize(445, 281)
        self.verticalLayout = QVBoxLayout(DialogDormSelection)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.column_view = QColumnView(DialogDormSelection)
        self.column_view.setObjectName(u"column_view")

        self.verticalLayout.addWidget(self.column_view)

        self.buttonBox = QDialogButtonBox(DialogDormSelection)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DialogDormSelection)
        self.buttonBox.accepted.connect(DialogDormSelection.accept)
        self.buttonBox.rejected.connect(DialogDormSelection.reject)

        QMetaObject.connectSlotsByName(DialogDormSelection)
    # setupUi

    def retranslateUi(self, DialogDormSelection):
        DialogDormSelection.setWindowTitle(QCoreApplication.translate("DialogDormSelection", u"\u9009\u62e9\u5bbf\u820d", None))
    # retranslateUi

