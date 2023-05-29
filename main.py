import sys
import psycopg2
import openpyxl
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QGraphicsScene
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from UIclass import main_window, LoginScreen, Add, delete, DeleteMessage, worker, add_worker


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
                self.publish_menu = PublishMenu(self.connection, self.cursor, self.current_user, self.departament, self.role_group)
                self.publish_menu.show()
            elif self.role_group == 'registry':
                self.departament = self.cursor.fetchone()[0]
                self.shop_menu = ShopMenu(self.connection, self.cursor, self.current_user, self.role_group)
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
        """
        self.Queries_button.clicked.connect(self.queries)
        """
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
    """def queries(self):
        self.q = Queries(self.connection, self.cursor)
        self.q.show()"""


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
        elif role_group == 'publish_manager':
            self.table.addItem('Книга')
            self.table.addItem('Автор')
            self.table.addItem('Издательство')
        elif role_group == 'shop_manager':
            self.table.addItem('Книга в магазине')
            self.table.addItem('Магазин')
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
        self.acc = Delete(self.connection, self.cursor, self.role_group)
        self.acc.show()

    def to_add(self):
        add = Add(self.connection, self.cursor, role_group='sobes_admin')
        add.exec_()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthWindow()

    window.show()
    sys.exit(app.exec_())
