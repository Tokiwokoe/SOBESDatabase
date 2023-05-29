# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Auth(object):
    def setupUi(self, Auth):
        Auth.setObjectName("Auth")
        Auth.resize(290, 230)
        Auth.setStyleSheet("background-color: rgb(230, 225, 198)")
        self.login = QtWidgets.QPushButton(Auth)
        self.login.setGeometry(QtCore.QRect(40, 180, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.login.setFont(font)
        self.login.setStyleSheet("font-size: 16px;\n"
"background-color: rgb(245, 245, 245)")
        self.login.setObjectName("login")
        self.loginfield = QtWidgets.QLineEdit(Auth)
        self.loginfield.setGeometry(QtCore.QRect(110, 70, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.loginfield.setFont(font)
        self.loginfield.setStyleSheet("font-size: 16px;\n"
"font: \"Sitka Text\";\n"
"background-color: rgb(245, 245, 245)")
        self.loginfield.setText("")
        self.loginfield.setObjectName("loginfield")
        self.passwordfield = QtWidgets.QLineEdit(Auth)
        self.passwordfield.setGeometry(QtCore.QRect(110, 110, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.passwordfield.setFont(font)
        self.passwordfield.setStyleSheet("font-size: 16px;\n"
"font: \"Sitka Text\";\n"
"background-color: rgb(245, 245, 245)")
        self.passwordfield.setText("")
        self.passwordfield.setObjectName("passwordfield")
        self.label = QtWidgets.QLabel(Auth)
        self.label.setGeometry(QtCore.QRect(30, 70, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
"font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Auth)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);\n"
"font-size: 16px;\n"
"font: \"Yu Gothic UI Semibold\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Auth)
        self.label_3.setGeometry(QtCore.QRect(0, 10, 291, 41))
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
        self.error = QtWidgets.QLabel(Auth)
        self.error.setGeometry(QtCore.QRect(0, 150, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.error.setFont(font)
        self.error.setStyleSheet("color: red;\n"
"font-size: 16px;\n"
"font: \"Sitka Text\";")
        self.error.setText("")
        self.error.setAlignment(QtCore.Qt.AlignCenter)
        self.error.setObjectName("error")

        self.retranslateUi(Auth)
        QtCore.QMetaObject.connectSlotsByName(Auth)

    def retranslateUi(self, Auth):
        _translate = QtCore.QCoreApplication.translate
        Auth.setWindowTitle(_translate("Auth", "Авторизация"))
        self.login.setText(_translate("Auth", "Войти"))
        self.label.setText(_translate("Auth", "Логин:"))
        self.label_2.setText(_translate("Auth", "Пароль:"))
        self.label_3.setText(_translate("Auth", "Вход"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Auth = QtWidgets.QDialog()
    ui = Ui_Auth()
    ui.setupUi(Auth)
    Auth.show()
    sys.exit(app.exec_())
