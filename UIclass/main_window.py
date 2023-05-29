# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 720)
        MainWindow.setStyleSheet("background-color: rgb(230, 225, 198)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.client = QtWidgets.QPushButton(self.centralwidget)
        self.client.setGeometry(QtCore.QRect(10, 60, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.client.setFont(font)
        self.client.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.client.setObjectName("client")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(260, 0, 751, 671))
        self.tableWidget.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.Change_button = QtWidgets.QPushButton(self.centralwidget)
        self.Change_button.setGeometry(QtCore.QRect(10, 473, 241, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Change_button.setFont(font)
        self.Change_button.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.Change_button.setObjectName("Change_button")
        self.Workers_button = QtWidgets.QPushButton(self.centralwidget)
        self.Workers_button.setGeometry(QtCore.QRect(10, 573, 241, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Workers_button.setFont(font)
        self.Workers_button.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.Workers_button.setObjectName("Workers_button")
        self.Queries_button = QtWidgets.QPushButton(self.centralwidget)
        self.Queries_button.setGeometry(QtCore.QRect(10, 623, 241, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Queries_button.setFont(font)
        self.Queries_button.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.Queries_button.setObjectName("Queries_button")
        self.Delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.Delete_button.setGeometry(QtCore.QRect(10, 523, 241, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Delete_button.setFont(font)
        self.Delete_button.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.Delete_button.setObjectName("Delete_button")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 420, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font-size: 32px;\n"
"font: \"Arial Black\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);\n"
"font-size: 32px;\n"
"font: \"Arial Black\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.client_type = QtWidgets.QPushButton(self.centralwidget)
        self.client_type.setGeometry(QtCore.QRect(10, 360, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.client_type.setFont(font)
        self.client_type.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.client_type.setObjectName("client_type")
        self.dist = QtWidgets.QPushButton(self.centralwidget)
        self.dist.setGeometry(QtCore.QRect(10, 310, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.dist.setFont(font)
        self.dist.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.dist.setObjectName("dist")
        self.help = QtWidgets.QPushButton(self.centralwidget)
        self.help.setGeometry(QtCore.QRect(10, 110, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.help.setFont(font)
        self.help.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.help.setObjectName("help")
        self.help_type = QtWidgets.QPushButton(self.centralwidget)
        self.help_type.setGeometry(QtCore.QRect(10, 260, 240, 40))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.help_type.setFont(font)
        self.help_type.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.help_type.setObjectName("help_type")
        self.organ = QtWidgets.QPushButton(self.centralwidget)
        self.organ.setGeometry(QtCore.QRect(10, 160, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.organ.setFont(font)
        self.organ.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.organ.setObjectName("organ")
        self.exemption = QtWidgets.QPushButton(self.centralwidget)
        self.exemption.setGeometry(QtCore.QRect(10, 210, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.exemption.setFont(font)
        self.exemption.setStyleSheet("font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";\n"
"background-color: rgb(245, 245, 245)")
        self.exemption.setObjectName("exemption")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.client.setText(_translate("MainWindow", "Клиенты"))
        self.Change_button.setText(_translate("MainWindow", "Добавить данные в таблицы"))
        self.Workers_button.setText(_translate("MainWindow", "Редактировать пользователей"))
        self.Queries_button.setText(_translate("MainWindow", "Перейти в режим запросов"))
        self.Delete_button.setText(_translate("MainWindow", "Удаление из таблицы"))
        self.label_2.setText(_translate("MainWindow", "Изменение"))
        self.label_3.setText(_translate("MainWindow", "Просмотр"))
        self.client_type.setText(_translate("MainWindow", "Типы клиента"))
        self.dist.setText(_translate("MainWindow", "Район"))
        self.help.setText(_translate("MainWindow", "Помощь"))
        self.help_type.setText(_translate("MainWindow", "Виды помощи"))
        self.organ.setText(_translate("MainWindow", "Учреждения"))
        self.exemption.setText(_translate("MainWindow", "Льготы"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())