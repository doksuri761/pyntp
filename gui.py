# -*- coding: utf-8 -*-

from threading import Thread
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import ntplib
from time import ctime, sleep, time
import sys


class Ui_Dialog(object):
    def __init__(self):
        self.thread_run = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("K-utc")
        Dialog.resize(400, 150)
        icon = QIcon()
        icon.addFile(u"icon.jpeg", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.print = QLabel(Dialog)
        self.print.setGeometry(QRect(15, 5, 371, 91))
        self.print.setObjectName("print")
        self.host = QLineEdit(Dialog)
        self.host.setGeometry(QRect(12, 120, 181, 21))
        self.host.setObjectName("host")
        self.interval = QDoubleSpinBox(Dialog)
        self.interval.setGeometry(QRect(211, 120, 71, 21))
        self.interval.setObjectName("interval")
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setGeometry(QRect(314, 120, 71, 21))
        self.pushButton.setObjectName("pushButton")
        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(self.thread_f)
        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def update(self, host, interval):
        ntpcli = ntplib.NTPClient()
        while self.thread_run:
            start_time = time()
            try:
                res = ntpcli.request(host)
                text = ""
                text += "------------------------------------\n"
                text += f"offset: {res.offset}\n"
                text += f"tx time: {ctime(res.tx_time)}\n"
                text += f"local time: {datetime.now().ctime()}\n"
                text += f"time elapsed: {time() - start_time}\n"
                text += "------------------------------------"
                self.print.setText(text)
                sleep(abs(interval - (time() - start_time)))
            except ntplib.NTPException:
                pass
        self.print.setText("1. ntp 서버의 주소 or ip 입력\n2. 인터벌 설정\n3. start")

    def thread_f(self):
        if self.thread_run is None or not self.thread_run:
            self.thread_run = True
            host = self.host.text()
            interval = self.interval.value()
            self.thread = Thread(target=self.update, args=(host, interval))
            self.thread.start()
        else:
            self.thread_run = False


    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Ktc delay tester", None))
        self.print.setText(QCoreApplication.translate("Dialog", u"1. ntp 서버의 주소 or ip 입력\n2. 인터벌 설정\n3. start", None))
        self.pushButton.setText(_translate("Dialog", "start"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
