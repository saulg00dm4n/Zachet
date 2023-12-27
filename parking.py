import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox
import sqlite3


class ParkingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для парковки")
        self.setGeometry(100, 100, 300, 200)

        self.label1 = QLabel("Номер пропуска:")
        self.label2 = QLabel("Номер парковочного места:")
        self.textbox1 = QLineEdit()
        self.textbox2 = QLineEdit()
        self.button1 = QPushButton("Выписать талон")
        self.button2 = QPushButton("Удалить информацию")

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.label2)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button1.clicked.connect(self.issue_parking_ticket)
        self.button2.clicked.connect(self.delete_parking_info)

        self.create_database()

    def create_database(self):
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employees
                     (pass_number TEXT, space_number INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS guests
                     (pass_number TEXT, space_number INTEGER)''')
        c.close()

    def issue_parking_ticket(self):
        pass_number = self.textbox1.text()
        space_number = int(self.textbox2.text())

        if len(pass_number) == 0:
            self.show_error_message("Введите номер пропуска!")
            return

        if space_number <= 0 or space_number > 20:
            self.show_error_message("Некорректный номер парковочного места!")
            return

        if self.check_space_availability(space_number, "employees"):
            self.assign_parking_space(pass_number, space_number, "employees")
        elif self.check_space_availability(space_number, "guests"):
            self.assign_parking_space(pass_number, space_number, "guests")
        else:
            self.show_error_message("Все парковочные места заняты!")

    def check_space_availability(self, space_number, table_name):
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name} WHERE space_number = ?", (space_number,))
        data = c.fetchone()
        c.close()
        return data is None

    def assign_parking_space(self, pass_number, space_number, table_name):
        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO {table_name} (pass_number, space_number) VALUES (?, ?)", (pass_number, space_number))
        conn.commit()
        c.close()
        self.show_info_message(f"Парковочное место {space_number} выдано сотруднику с пропуском {pass_number}")

    def delete_parking_info(self):
        pass_number = self.textbox1.text()

        if len(pass_number) == 0:
            self.show_error_message("Введите номер пропуска!")
            return

        conn = sqlite3.connect('parking.db')
        c = conn.cursor()
        c.execute("DELETE FROM employees WHERE pass_number = ?", (pass_number,))
        c.execute("DELETE FROM guests WHERE pass_number = ?", (pass_number,))
        conn.commit()
        c.close()
        self.show_info_message(f"Информация о сотруднике с пропуском {pass_number} удалена")

    def show_error_message(self, message):
        self.show_message_box("Ошибка", message)

    def show_info_message(self, message):
        self.show_message_box("Информация", message)

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parking_app = ParkingApp()
    parking_app.show()
    sys.exit(app.exec())