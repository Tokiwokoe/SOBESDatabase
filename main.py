import sys
import psycopg2
import openpyxl
import datetime
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QGraphicsScene
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from UIclass import main_window, LoginScreen, Add, delete, DeleteMessage, worker, add_worker, accountant, add_help, registry, add_client, graphics, queries


class AuthWindow(QMainWindow, LoginScreen.Ui_Auth):
    def __init__(self):
        super(AuthWindow, self).__init__()
        self.setupUi(self)
        self.login.clicked.connect(self.to_login)

    def to_login(self):
        try:
            self.user = self.loginfield.text()
            self.password = self.passwordfield.text()
            self.connection = psycopg2.connect(
                host='localhost',
                database='Sobes',
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT current_user;")
            self.current_user = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT rolname FROM pg_user JOIN pg_auth_members ON pg_user.usesysid = pg_auth_members.member JOIN pg_roles ON pg_roles.oid = pg_auth_members.roleid WHERE pg_user.usename = current_user;")
            self.role_group = self.cursor.fetchone()[0]
            print(f'{self.current_user} из группы {self.role_group} вошёл в систему')
            if self.role_group == 'sobes_admin':
                self.admin_menu = MainMenu(self.connection, self.cursor, self.current_user, self.role_group)
                self.admin_menu.show()
            elif self.role_group == 'accountant':
                self.cursor.execute(f"SELECT departament FROM \"accountant\" WHERE login = '{self.user}'")
                self.departament = self.cursor.fetchone()[0]
                self.publish_menu = AccountantMenu(self.connection, self.cursor, self.current_user, self.departament, self.role_group)
                self.publish_menu.show()
            elif self.role_group == 'registry':
                self.shop_menu = RegistryMenu(self.connection, self.cursor, self.current_user, self.role_group)
                self.shop_menu.show()
            else:
                self.error.setText('Неизвестная роль')
            self.close()

        except psycopg2.Error as err:
            print(err)
            self.error.setText('Проверьте ввод')


class PrintTable(QMainWindow):
    def __init__(self):
        super(PrintTable, self).__init__()

    def to_print_table(self, query):
        self.cursor.execute(query)
        self.rows = self.cursor.fetchall()
        self.tableWidget.setRowCount(len(self.rows))
        self.tableWidget.setColumnCount(len(self.labels))
        self.tableWidget.setHorizontalHeaderLabels(self.labels)
        i = 0
        for elem in self.rows:
            j = 0
            for t in elem:
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        i = 0
        self.tableWidget.resizeColumnsToContents()

    def to_print_client(self):
        query = 'SELECT * FROM "Client_view"'
        self.labels = ['id', 'ФИО', 'Дата рождения', 'Тип клиента', 'Пенсия', 'Льгота']
        self.to_print_table(query)

    def to_print_client_type(self):
        query = 'SELECT * FROM "Client_type_view"'
        self.labels = ['id', 'Тип клиента']
        self.to_print_table(query)

    def to_print_dist(self):
        query = 'SELECT * FROM "District_view"'
        self.labels = ['id', 'Район']
        self.to_print_table(query)

    def to_print_exemption(self):
        query = 'SELECT * FROM "Exemption_view"'
        self.labels = ['id', 'Льгота']
        self.to_print_table(query)

    def to_print_help(self):
        query = 'SELECT * FROM "Help_view"'
        self.labels = ['Клиент', 'Адрес учреждения', 'Вид помощи', 'Денежный эквивалент', 'Дата выдачи']
        self.to_print_table(query)

    def to_print_help_type(self):
        query = 'SELECT * FROM "Help_type_view"'
        self.labels = ['id', 'Вид помощи']
        self.to_print_table(query)

    def to_print_organ(self):
        query = 'SELECT * FROM "Organ_view"'
        self.labels = ['id', 'Район', 'Год открытия', 'Количество сотрудников', 'Адрес', 'Номер телефона']
        self.to_print_table(query)

    def to_print_acc(self):
        query = 'SELECT id, login, departament FROM "accountant" ORDER BY id'
        self.labels = ['id', 'Логин', 'Учреждение']
        self.to_print_table(query)


class MainMenu(PrintTable, main_window.Ui_MainWindow):
    def __init__(self, connection, cursor, current_user, role_group):
        super(MainMenu, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1020, 720)
        self.client.clicked.connect(self.to_print_client)
        self.client_type.clicked.connect(self.to_print_client_type)
        self.dist.clicked.connect(self.to_print_dist)
        self.exemption.clicked.connect(self.to_print_exemption)
        self.help.clicked.connect(self.to_print_help)
        self.help_type.clicked.connect(self.to_print_help_type)
        self.organ.clicked.connect(self.to_print_organ)
        self.Change_button.clicked.connect(self.to_add)
        self.Delete_button.clicked.connect(self.to_delete)
        self.Workers_button.clicked.connect(self.to_add_worker)
        self.Queries_button.clicked.connect(self.queries)
        self.connection = connection
        self.cursor = cursor
        self.current_user = current_user
        self.role_group = role_group

    def to_add(self):
        self.add = Add(self.connection, self.cursor, self.role_group)
        self.add.show()

    def to_delete(self):
        self.delete = Delete(self.connection, self.cursor, self.role_group)
        self.delete.show()

    def to_add_worker(self):
        self.worker = AddWorker(self.connection, self.cursor, self.current_user, self.role_group)
        self.worker.show()

    def queries(self):
        self.q = Queries(self.connection, self.cursor)
        self.q.show()


class Add(QMainWindow, Add.Ui_Dialog):
    def __init__(self, connection, cursor, role_group):
        super(Add, self).__init__()
        self.setupUi(self)
        self.role_group = role_group
        self.connection = connection
        self.cursor = cursor
        if role_group == 'sobes_admin':
            self.table.addItem('Район')
            self.table.addItem('Льготы')
            self.table.addItem('Вид помощи')
            self.table.addItem('Тип клиента')
        self.OKbutton.clicked.connect(self.to_add)

    def to_add(self):
        if self.table.currentText() == 'Район':
            self.table_name = '"District"'
        elif self.table.currentText() == 'Льготы':
            self.table_name = '"Exemption"'
        elif self.table.currentText() == 'Вид помощи':
            self.table_name = '"Help_type"'
        elif self.table.currentText() == 'Тип клиента':
            self.table_name = '"Client_type"'
        try:
            self.name = self.id.text()
            query = f'SELECT id FROM {self.table_name} ORDER BY id DESC LIMIT 1'
            self.cursor.execute(query)
            self.name_id = self.cursor.fetchone()
            if not self.name_id:
                self.name_id = [0]
            query = f"INSERT INTO {self.table_name} VALUES({int(self.name_id[0]) + 1}, '{self.name}')"
            self.cursor.execute(query)
            self.connection.commit()
            self.error.setText('Успешно добавлено')
        except Exception as err:
            print(err)
            self.error.setText('Ошибка!')


class DeleteMess(QMainWindow, DeleteMessage.Ui_Dialog):
    def __init__(self, connection, cursor, table, id):
        super(DeleteMess, self).__init__()
        self.setupUi(self)
        self.setFixedSize(560, 150)
        self.connection = connection
        self.cursor = cursor
        self.table = table
        self.id = id
        query = f'SELECT * FROM {self.table} WHERE id = {self.id}'
        self.cursor.execute(query)
        self.text.setText(f'Вы действительно хотите удалить {self.cursor.fetchall()}')
        self.OKbutton.clicked.connect(self.delete)
        self.CancelButton.clicked.connect(self.cancel)

    def delete(self):
        try:
            query = f'DELETE FROM {self.table} WHERE id = {self.id}'
            self.cursor.execute(query)
            self.connection.commit()
            self.error.setText('Удалено!')
        except Exception as err:
            print(err)
            self.error.setText('Ошибка!')

    def cancel(self):
        self.close()


class Delete(QMainWindow, delete.Ui_Dialog):
    def __init__(self, connection, cursor, role_group):
        super(Delete, self).__init__()
        self.setupUi(self)
        self.role_group = role_group
        self.connection = connection
        self.cursor = cursor
        if role_group == 'sobes_admin':
            self.table.addItem('Район')
            self.table.addItem('Льготы')
            self.table.addItem('Вид помощи')
            self.table.addItem('Тип клиента')
            self.table.addItem('Бухгалтер')
            self.table.addItem('Регистратура')
        elif role_group == 'accountant':
            self.table.addItem('Выданная помощь')
        elif role_group == 'registry':
            self.table.addItem('Клиенты')
        self.OKbutton.clicked.connect(self.to_delete)

    def to_delete(self):
        if self.table.currentText() == 'Район':
            self.table_name = '"District"'
        elif self.table.currentText() == 'Льготы':
            self.table_name = '"Exemption"'
        elif self.table.currentText() == 'Вид помощи':
            self.table_name = '"Help_type"'
        elif self.table.currentText() == 'Тип клиента':
            self.table_name = '"Client_type"'
        elif self.table.currentText() == 'Бухгалтер':
            self.table_name = '"accountant"'
        elif self.table.currentText() == 'Регистратура':
            self.table_name = '"registry"'
        elif self.table.currentText() == 'Выданная помощь':
            self.table_name = '"Help"'
        elif self.table.currentText() == 'Клиенты':
            self.table_name = '"Client"'
        id = self.id.text()
        self.message = DeleteMess(self.connection, self.cursor, self.table_name, id)
        self.message.show()


class AddWorker(PrintTable, worker.Ui_Dialog):
    def __init__(self, connection, cursor, current_user, role_group):
        super(AddWorker, self).__init__()
        self.setupUi(self)
        self.setFixedSize(550, 580)
        self.connection = connection
        self.cursor = cursor
        self.current_user = current_user
        self.role_group = role_group
        self.update_reg.clicked.connect(self.to_print_reg)
        self.update_acc.clicked.connect(self.to_print_acc)
        self.add_acc.clicked.connect(self.to_add)
        self.add_reg.clicked.connect(self.to_add)
        self.delete_reg.clicked.connect(self.to_delete)
        self.delete_acc.clicked.connect(self.to_delete)

    def to_delete(self):
        self.delete = Delete(self.connection, self.cursor, self.role_group)
        self.delete.show()

    def to_add(self):
        self.add = AddEmployees(self.connection, self.cursor)
        self.add.show()

    def to_print_reg(self):
        query = 'SELECT id, login FROM "registry" ORDER BY id'
        self.labels = ['id', 'Логин']
        self.cursor.execute(query)
        self.rows = self.cursor.fetchall()
        self.tableWidget_2.setRowCount(len(self.rows))
        self.tableWidget_2.setColumnCount(len(self.labels))
        self.tableWidget_2.setHorizontalHeaderLabels(self.labels)
        i = 0
        for elem in self.rows:
            j = 0
            for t in elem:
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        i = 0
        self.tableWidget_2.resizeColumnsToContents()


class AddEmployees(QMainWindow, add_worker.Ui_Dialog):
    def __init__(self, connection, cursor):
        super(AddEmployees, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.table.addItem('Бухгалтер')
        self.table.addItem('Регистратура')
        self.table_name = 'accountant'
        self.table.currentTextChanged.connect(self.handle_table_change)  # Подключение сигнала
        self.add_button.clicked.connect(self.to_add)

    def handle_table_change(self):
        if self.table.currentText() == 'Бухгалтер':
            self.table_name = 'accountant'
            self.dep.show()
            self.label_6.show()
        if self.table.currentText() == 'Регистратура':
            self.table_name = 'registry'
            self.dep.hide()
            self.label_6.hide()

    def to_add(self):
        self.query = f'SELECT id FROM {self.table_name} ORDER BY id DESC'
        self.cursor.execute(self.query)
        self.id = self.cursor.fetchall()
        if not self.id:
            self.id = [0]
        if self.table_name == 'accountant':
            self.query = f"INSERT INTO {self.table_name} VALUES ({self.id[0]+1}, '{self.log.text()}', {self.dep.text()})"
        else:
            self.query = f"INSERT INTO {self.table_name} VALUES ({self.id[0] + 1}, '{self.log.text()}')"
        try:
            self.cursor.execute(self.query)
            self.connection.commit()
            self.error.setText('Успешно добавлено')
        except Exception as err:
            print(err)
            self.error.setText('Ошибка!')


class AccountantMenu(PrintTable, accountant.Ui_Dialog):
    def __init__(self, connection, cursor, current_user, departament, role_group):
        super(AccountantMenu, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.current_user = current_user
        self.departament = departament
        self.role_group = role_group
        self.auth_as.setText(f'Вы вошли как: {current_user}, учреждение № {self.departament}')
        self.Update_btn.clicked.connect(self.to_print_help)
        self.Add_btn.clicked.connect(self.to_add_help)
        self.Delete_btn.clicked.connect(self.to_delete)

    def to_delete(self):
        self.delete = Delete(self.connection, self.cursor, self.role_group)
        self.delete.show()

    def to_add_help(self):
        self.add = AddHelp(self.connection, self.cursor, self.departament)
        self.add.show()


class RegistryMenu(PrintTable, registry.Ui_Dialog):
    def __init__(self, connection, cursor, current_user, role_group):
        super(RegistryMenu, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.current_user = current_user
        self.role_group = role_group
        self.auth_as.setText(f'Вы вошли как: {current_user}')
        self.Update_btn.clicked.connect(self.to_print_client)
        self.Add_btn.clicked.connect(self.to_add_client)
        self.Delete_btn.clicked.connect(self.to_delete)

    def to_delete(self):
        self.delete = Delete(self.connection, self.cursor, self.role_group)
        self.delete.show()

    def to_add_client(self):
        self.add = AddClient(self.connection, self.cursor)
        self.add.show()


class AddHelp(QMainWindow, add_help.Ui_Dialog):
    def __init__(self, connection, cursor, departament):
        super(AddHelp, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.departament = departament
        query = 'SELECT id, name FROM "Client"'
        self.cursor.execute(query)
        for t in self.cursor.fetchall():
            self.client.addItem(str(t))
        query = 'SELECT id, name FROM "Help_type"'
        self.cursor.execute(query)
        for t in self.cursor.fetchall():
            self.help_type.addItem(str(t))
        self.Add.clicked.connect(self.correct_data)

    def correct_data(self):
        money = self.money.text()
        client = self.client.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        help_type = self.help_type.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        client_id = str(client[0])
        help_type_id = str(help_type[0])
        if int(money) > 0:
            try:
                query = f"INSERT INTO \"Help\" VALUES({client_id}, {self.departament}, {help_type_id}, {money}, '{datetime.date.today()}')"
                self.cursor.execute(query)
                self.connection.commit()
                self.error.setText('Успешно добавлено')
            except Exception as err:
                print(err)
                self.error.setText('Что-то пошло не так :(')
        else:
            self.error.setText('Проверьте корректность заполнения полей!')


class AddClient(QMainWindow, add_client.Ui_Dialog):
    def __init__(self, connection, cursor):
        super(AddClient, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        query = 'SELECT id, name FROM "Client_type"'
        self.cursor.execute(query)
        for t in self.cursor.fetchall():
            self.client_type.addItem(str(t))
        query = 'SELECT id, name FROM "Exemption"'
        self.cursor.execute(query)
        for t in self.cursor.fetchall():
            self.exemption.addItem(str(t))
        self.Add.clicked.connect(self.correct_data)

    def correct_data(self):
        name = self.name.text()
        birth_date = self.birth.text()
        client_type = self.client_type.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        exemption = self.exemption.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        client_type_id = str(client_type[0])
        exemption_id = str(exemption[0])
        pension = self.pension.text()
        if int(pension) > 0:
            try:
                query = f'SELECT id FROM "Client" ORDER BY id DESC LIMIT 1'
                self.cursor.execute(query)
                self.name_id = self.cursor.fetchone()
                if not self.name_id:
                    self.name_id = [0]
                query = f"INSERT INTO \"Client\" VALUES({int(self.name_id[0])+1}, '{name}', '{birth_date}', {client_type_id}, {pension}, {exemption_id})"
                self.cursor.execute(query)
                self.connection.commit()
                self.error.setText('Успешно добавлено')
            except Exception as err:
                print(err)
                self.error.setText('Что-то пошло не так :(')
        else:
            self.error.setText('Проверьте корректность заполнения полей!')


class Queries(QMainWindow, queries.Ui_Dialog):
    def __init__(self, connection, cursor):
        super(Queries, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.queries.currentTextChanged.connect(self.handle_queries_change)  # Подключение сигнала
        self.queries.addItem('Адрес, телефон, учреждения заданного района. Симметричное внутреннее соединение с условием отбора по внешнему ключу')
        self.queries.addItem('ФИО, дата рождения клиента с выбранной льготой. Симметричное внутреннее соединение с условием отбора по внешнему ключу')
        self.queries.addItem('Клиент, адрес учреждения, вид помощи, денежный эквивалент помощи, выданной в указанную дату. Симметричное внутреннее соединение с условием отбора по датам')
        self.queries.addItem('Адрес, телефон, год открытия, район учреждения, открытого в заданный год. Симметричное внутреннее соединение с условием отбора по датам')
        self.queries.addItem('Адрес, телефон, год открытия, район учреждения. Симметричное внутреннее соединение без условия')
        self.queries.addItem('Клиент и его тип. Симметричное внутреннее соединение без условия')
        self.queries.addItem('Клиент и его льгота. Симметричное внутреннее соединение без условия')
        self.queries.addItem('ФИО, дата рождения по заданному типу клиента. Левое внешнее соединение')
        self.queries.addItem('ФИО, дата рождения по заданному типу клиента. Правое внешнее соединение')
        self.queries.addItem('ID клиента, ФИО, дата рождения, тип по заданному имени. Запрос на запросе по принципу левого соединения')
        self.queries.addItem('Учреждение и количество оказанной помощи. Итоговый запрос без условия')
        self.queries.addItem('Учреждения в заданном промежутке и количество оказанной помощи. Итоговый запрос с условием на данные')
        self.queries.addItem('Учреждения с количеством оказанной помощи больше заданного. Итоговый запрос с условием на группы')
        self.queries.addItem('Учреждения в заданном промежутке и с количеством оказанной помощи больше заданного. Итоговый запрос с условием на данные и на группы')
        self.queries.addItem('Учреждения с количеством оказанной помощи. Запрос на запросе по принципу итогового запроса')
        self.queries.addItem('Учреждения с количеством оказанной помощи. Запрос с подзапросом')

    def handle_queries_change(self):
        if self.queries.currentText() == 'Адрес, телефон, учреждения заданного района. Симметричное внутреннее соединение с условием отбора по внешнему ключу':
            self.hide_all()
            self.label_combo.show()
            self.label_combo.setText('Выберите район')
            self.comboBox.show()
            query = 'SELECT id, name FROM "District"'
            self.cursor.execute(query)
            for t in self.cursor.fetchall():
                self.comboBox.addItem(str(t))
            district = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
            district_id = str(district[0])
            self.labels = ['Адрес', 'Телефон', 'Район']
            self.query = f'SELECT * FROM q1({district_id})'
            self.comboBox.currentTextChanged.connect(self.q1)
        elif self.queries.currentText() == 'ФИО, дата рождения клиента с выбранной льготой. Симметричное внутреннее соединение с условием отбора по внешнему ключу':
            self.hide_all()
            self.hide_all()
            self.label_combo.show()
            self.comboBox.show()
            self.label_combo.setText('Выберите льготу')
            self.comboBox.show()
            query = 'SELECT id, name FROM "Exemption"'
            self.cursor.execute(query)
            for t in self.cursor.fetchall():
                self.comboBox.addItem(str(t))
            exemption = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
            exemption_id = str(exemption[0])
            self.labels = ['ФИО', 'Дата рождения', 'Льгота']
            self.query = f'SELECT * FROM q2({exemption_id})'
            self.comboBox.currentTextChanged.connect(self.q2)
        elif self.queries.currentText() == 'Клиент, адрес учреждения, вид помощи, денежный эквивалент помощи, выданной в указанную дату. Симметричное внутреннее соединение с условием отбора по датам':
            self.hide_all()
            self.dateEdit.show()
            self.label_date.show()
            self.label_date.setText('Введите дату')
            self.dateEdit.dateChanged.connect(self.q3)  # Подключение сигнала
        elif self.queries.currentText() == 'Адрес, телефон, год открытия, район учреждения, открытого в заданный год. Симметричное внутреннее соединение с условием отбора по датам':
            self.hide_all()
            self.hide_all()
            self.label_text.show()
            self.textEdit.show()
            self.textEdit.setText('')
            self.label_text.setText('Выберите год')
            self.textEdit.textChanged.connect(self.q4)
        elif self.queries.currentText() == 'Адрес, телефон, год открытия, район учреждения. Симметричное внутреннее соединение без условия':
            self.hide_all()
            self.labels = ['Адрес', 'Телефон', 'Год открытия', 'Район']
            self.query = 'SELECT * FROM q5()'
        elif self.queries.currentText() == 'Клиент и его тип. Симметричное внутреннее соединение без условия':
            self.hide_all()
            self.labels = ['ФИО', 'Тип клиента']
            self.query = 'SELECT * FROM q6()'
        elif self.queries.currentText() == 'Клиент и его льгота. Симметричное внутреннее соединение без условия':
            self.hide_all()
            self.labels = ['ФИО', 'Льгота']
            self.query = f'SELECT * FROM q7()'
        elif self.queries.currentText() == 'ФИО, дата рождения по заданному типу клиента. Левое внешнее соединение':
            self.hide_all()
            self.labels = ['ФИО', 'Дата рождения', 'Тип клиента']
            self.query = f'SELECT * FROM q8()'
        elif self.queries.currentText() == 'ФИО, дата рождения по заданному типу клиента. Правое внешнее соединение':
            self.hide_all()
            self.labels = ['ФИО', 'Дата рождения', 'Тип клиента']
            self.query = f'SELECT * FROM q9()'
        elif self.queries.currentText() == 'ID клиента, ФИО, дата рождения, тип по заданному имени. Запрос на запросе по принципу левого соединения':
            self.hide_all()
            self.textEdit.setText('')
            self.label_text.show()
            self.textEdit.show()
            self.label_text.setText('Выберите имя')
            self.textEdit.textChanged.connect(self.q10)
        elif self.queries.currentText() == 'Учреждение и количество оказанной помощи. Итоговый запрос без условия':
            self.hide_all()
            self.labels = ['Учреждение', 'Количество оказанной помощи']
            self.query = f'SELECT * FROM q11()'
        elif self.queries.currentText() == 'Учреждения в заданном промежутке и с количеством оказанной помощи больше заданного. Итоговый запрос с условием на данные':
            self.hide_all()
            self.label_text.show()
            self.textEdit.show()
            self.label_text_2.show()
            self.textEdit_2.show()
            self.textEdit.setText('')
            self.textEdit_2.setText('')
            self.label_text.setText('Выберите начальный ID учреждения')
            self.label_text_2.setText('Выберите конечный ID учреждения')
            self.textEdit.textChanged.connect(self.q12)
            self.textEdit_2.textChanged.connect(self.q12)
            self.excel_btn.show()
            self.graph_btn.show()
        elif self.queries.currentText() == 'Учреждения с количеством оказанной помощи больше заданного. Итоговый запрос с условием на группы':
            self.hide_all()
            self.label_text.show()
            self.textEdit.show()
            self.label_text.setText('Выберите количество оказанной помощи')
            self.textEdit.textChanged.connect(self.q13)
            self.excel_btn.show()
            self.graph_btn.show()
        elif self.queries.currentText() == 'Учреждения в заданном промежутке и с количеством оказанной помощи больше заданного. Итоговый запрос с условием на данные и на группы':
            self.hide_all()
            self.label_text.show()
            self.textEdit.show()
            self.label_text_2.show()
            self.textEdit_2.show()
            self.label_text_3.show()
            self.textEdit_3.show()
            self.textEdit.setText('')
            self.textEdit_2.setText('')
            self.label_text.setText('Выберите начальный ID учреждения')
            self.label_text_2.setText('Выберите конечный ID учреждения')
            self.label_text_3.setText('Выберите количество оказанной помощи')
            self.textEdit.textChanged.connect(self.q14)
            self.textEdit_2.textChanged.connect(self.q14)
            self.textEdit_3.textChanged.connect(self.q14)
            self.excel_btn.show()
            self.graph_btn.show()
        elif self.queries.currentText() == 'Учреждения с количеством оказанной помощи. Запрос на запросе по принципу итогового запроса':
            self.hide_all()
            self.label_text.show()
            self.textEdit.show()
            self.label_text.setText('Выберите количество книг')
            self.textEdit.textChanged.connect(self.q15)
            self.excel_btn.show()
            self.graph_btn.show()
        elif self.queries.currentText() == 'Учреждения с количеством оказанной помощи. Запрос с подзапросом':
            self.hide_all()
            self.label_combo.show()
            self.comboBox.show()
            self.label_combo.setText('Выберите район')
            self.comboBox.show()
            query = 'SELECT id, name FROM "District"'
            self.cursor.execute(query)
            for t in self.cursor.fetchall():
                self.comboBox.addItem(str(t))
            city = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
            city_id = str(city[0])
            self.labels = ['ID учреждения', 'Количество оказанной помощи']
            self.query = f'SELECT * FROM q16({city_id})'
            self.comboBox.currentTextChanged.connect(self.q16)
        self.print.clicked.connect(self.to_print)
        self.graph_btn.clicked.connect(self.create_chart)
        self.excel_btn.clicked.connect(self.export_to_excel)

    def hide_all(self):
        self.label_text.hide()
        self.textEdit.hide()
        self.label_combo.hide()
        self.comboBox.hide()
        self.label_text_2.hide()
        self.comboBox.clear()
        self.textEdit_2.hide()
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.label_text_3.hide()
        self.textEdit_3.hide()
        self.dateEdit.hide()
        self.label_date.hide()
        self.graph_btn.hide()
        self.excel_btn.hide()

    def q1(self):
        district = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        district_id = str(district[0])
        self.labels = ['Адрес', 'Телефон', 'Район']
        self.query = f'SELECT * FROM q1({district_id})'

    def q2(self):
        exemption = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        exemption_id = str(exemption[0])
        self.labels = ['ФИО', 'Дата рождения', 'Льгота']
        self.query = f'SELECT * FROM q2({exemption_id})'

    def q3(self):
        date = self.dateEdit.text()
        self.labels = ['ФИО', 'Адрес', 'Тип клиента', 'Пенсия']
        self.query = f"SELECT * FROM q3('{date}')"

    def q4(self):
        year = self.textEdit.text()
        self.labels = ['Адрес', 'Телефон', 'Год открытия', 'Район']
        self.query = f'SELECT * FROM q4({year})'

    def q10(self):
        name = self.textEdit.text()
        self.labels = ['id клиента', 'ФИО', 'Дата рождения', 'Тип клиента']
        self.query = f"SELECT * FROM q10('{name}')"

    def q12(self):
        organ1 = self.textEdit.text()
        organ2 = self.textEdit_2.text()
        self.labels = ['ID учреждения', 'Количество оказанной помощи']
        self.query = f'SELECT * FROM q12({organ1}, {organ2})'

    def q13(self):
        book_count = self.textEdit.text()
        self.labels = ['ID учреждения', 'Количество оказанной помощи']
        self.query = f'SELECT * FROM q13({book_count})'

    def q14(self):
        organ1 = self.textEdit.text()
        organ2 = self.textEdit_2.text()
        helps = self.textEdit_3.text()
        self.labels = ['ID учреждения', 'Количество оказанной помощи']
        self.query = f'SELECT * FROM q14({organ1}, {organ2}, {helps})'

    def q15(self):
        helps = self.textEdit.text()
        self.labels = ['ID учреждения', 'Количество оказанной помощи']
        self.query = f'SELECT * FROM q15({helps})'

    def q16(self):
        query = 'SELECT id, name FROM "District"'
        self.cursor.execute(query)
        for t in self.cursor.fetchall():
            self.comboBox.addItem(str(t))
        dist = self.comboBox.currentText().replace('(', '').replace(')', '').replace(' \'', '\'').split(',')
        dist_id = str(dist[0])
        self.query = f'SELECT * FROM q16({dist_id})'

    def create_chart(self):
        self.label = self.queries.currentText()
        self.chart = Chart(self.connection, self.cursor, self.query, self.label)
        self.chart.show()

    def to_print(self):
        try:
            self.cursor.execute(self.query)
            self.rows = self.cursor.fetchall()
            self.tableWidget.setRowCount(len(self.rows))
            self.tableWidget.setColumnCount(len(self.labels))
            self.tableWidget.setHorizontalHeaderLabels(self.labels)
            i = 0
            for elem in self.rows:
                j = 0
                for t in elem:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(t).strip()))
                    j += 1
                i += 1
            i = 0
            self.tableWidget.resizeColumnsToContents()
        except psycopg2.Error as err:
            print(err)
            self.error.setText('Проверьте ввод!')

    def export_to_excel(self):
        self.label = self.queries.currentText().split('. ')
        self.cursor = self.connection.cursor()
        book = openpyxl.Workbook()
        sheet = book.active
        self.cursor.execute(self.query)
        results = self.cursor.fetchall()
        i = 0
        for row in results:
            i += 1
            j = 1
            for col in row:
                cell = sheet.cell(row=i, column=j)
                cell.value = col
                j += 1
        try:
            book.save(f"{self.label[1]}.xlsx")
            self.error.setText('Успешно!')
        except Exception as err:
            print(err)
            self.error.setText('Ошибка!')


class Chart(QMainWindow, graphics.Ui_Dialog):
    def __init__(self, connection, cursor, query, label):
        super(Chart, self).__init__()
        self.setupUi(self)
        self.connection = connection
        self.cursor = cursor
        self.query = query
        self.label = label.split('. ')
        self.cursor.execute(self.query)
        self.graphics_name.setText(self.label[1])
        data = self.cursor.fetchall()
        categories = [str(row[0]) for row in data]
        values = [row[1] for row in data]
        series = QBarSeries()
        bar_set = QBarSet("Оказано помощи")
        for value in values:
            bar_set.append(value)
        bar_set.setColor(QColor('green'))
        series.append(bar_set)
        chart = QChart()
        chart.addSeries(series)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        axis_y = QValueAxis()
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        scene = QGraphicsScene()
        scene.addItem(chart)
        chart.setMinimumSize(500, 500)
        scene.setSceneRect(chart.rect())
        self.graphicsView.setScene(scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthWindow()

    window.show()
    sys.exit(app.exec_())
