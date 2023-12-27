import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDateTime, Qt
import sqlite3
from main2 import TerminalApp
from parking import ParkingApp
from parking_ import ParkingApp2

class True_open_in(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Терминал входа")
        self.setGeometry(700, 400, 250, 200)

        self.label = QLabel(self)
        self.label.setText("Сотрудник найден в базе данных!\n Проходите!")
        self.label.setGeometry(20, 20, 200, 30)

        self.button = QPushButton("Нужен талон на\nпарковку сотрудников", self)
        self.button.resize(150, 40)
        self.button.move(50, 60)
        self.button.clicked.connect(self.openParkingApp)

        self.button = QPushButton("Нужен талон на\nпарковку гостей", self)
        self.button.resize(150, 40)
        self.button.move(50, 120)
        self.button.clicked.connect(self.openParkingApp2)


    def openParkingApp(self):
        self.terminal = ParkingApp()
        self.terminal.show()

    def openParkingApp2(self):
        self.terminal = ParkingApp2()
        self.terminal.show()


class True_open_out(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Терминал выхода")
        self.setGeometry(20, 20, 200, 30)

        self.label = QLabel(self)
        self.label.setText("Сотрудник найден в базе данных!\n Проходите!")
        self.label.setGeometry(20, 20, 200, 30)

        self.button = QPushButton("Был взят талон на\nпарковку сотрудников", self)
        self.button.resize(150, 40)
        self.button.move(80, 50)
        self.button.clicked.connect(self.openParkingApp)

        self.button = QPushButton("Был взят талон на\nпарковку гостей", self)
        self.button.resize(150, 40)
        self.button.move(80, 50)
        self.button.clicked.connect(self.openParkingApp2)

    def openParkingApp(self):
        self.terminal = ParkingApp()
        self.terminal.show()

    def openParkingApp2(self):
        self.terminal = ParkingApp2()
        self.terminal.show()

class False_open_in(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Терминал входа")
        self.setGeometry(700, 400, 300, 150)

        self.label = QLabel(self)
        self.label.setText("Сотрудник не найден в базе данных!\n Хотите оформить временный пропуск?")
        self.label.setGeometry(20, 20, 300, 30)

        self.button = QPushButton("Оформить", self)
        self.button.move(100, 80)
        self.button.clicked.connect(self.openTerminalApp)

    def openTerminalApp(self):
        self.terminal = TerminalApp()
        self.terminal.show()

class False_open_out(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Терминал выхода")
        self.setGeometry(700, 400, 300, 150)

        self.label = QLabel(self)
        self.label.setText("Сотрудник не найден в базе данных!\n "
                           "Просьба обратиться к старшему сотруднику\n "
                           "охранной службы.")
        self.label.setGeometry(20, 20, 300, 50)



class Terminal_open(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Терминал входа")
        self.setGeometry(700, 400, 300, 150)

class CheckDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Терминал охранника")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.last_name_label = QLabel("Фамилия:")
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)

        self.number_label = QLabel("Номер:")
        self.number_input = QLineEdit()
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_input)


        self.button_in = QPushButton("Вход", self)
        layout.addWidget(self.button_in)
        self.button_in.clicked.connect(self.check_data_in)

        self.button_out = QPushButton("Выход", self)
        layout.addWidget(self.button_out)
        self.button_out.clicked.connect(self.check_data_out)


    def check_data_in(self):
        name = self.name_input.text()
        last_name = self.last_name_input.text()
        number = self.number_input.text()

        conn1 = sqlite3.connect("person_data.db")
        cur1 = conn1.cursor()

        cur1.execute(
            "CREATE TABLE IF NOT EXISTS person_data (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, number INTEGER, expiration_time TEXT)")

        cur1.execute("SELECT * FROM person_data WHERE first_name=? AND last_name=? AND number=?", (name, last_name, number))
        data = cur1.fetchone()

        if data:
            self.open_window_T_in()

            connection1 = sqlite3.connect("attendance.db")
            cursor1 = connection1.cursor()
            current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

            cursor1.execute("INSERT INTO employees (pass_number, name, surname, entry_time) VALUES (?, ?, ?, ?)",
                                (number, name, last_name, current_time))
            connection1.commit()
            cursor1.close()
            connection1.close()

        else:
            self.open_window_F_in()

        conn1.commit()
        conn1.close()


    def check_data_out(self):
        name = self.name_input.text()
        last_name = self.last_name_input.text()
        number = self.number_input.text()

        conn2 = sqlite3.connect("person_data.db")
        cur2 = conn2.cursor()

        cur2.execute("SELECT * FROM person_data WHERE first_name=? AND last_name=? AND number=?", (name, last_name, number))
        data = cur2.fetchone()

        if data:
            self.open_window_T_out()

            connection2 = sqlite3.connect("attendance.db")
            cursor2 = connection2.cursor()
            current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

            cursor2.execute("UPDATE employees SET exit_time = ? WHERE pass_number = ?",
                                (current_time, number))
            connection2.commit()

            cursor2.close()
            connection2.close()

        else:
            self.open_window_F_out()

        cur2.close()
        conn2.close()

    def open_window_T_in(self):
        self.op_window = True_open_in()
        self.op_window.show()

    def open_window_T_out(self):
        self.op_window = True_open_out()
        self.op_window.show()

    def open_window_F_in(self):
        self.fl_window = False_open_in()
        self.fl_window.show()

    def open_window_F_out(self):
        self.fl_window = False_open_out()
        self.fl_window.show()

app = QApplication(sys.argv)
window = CheckDataWindow()
window.show()
sys.exit(app.exec())