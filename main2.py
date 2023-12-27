import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QDateTime, Qt, QTimer, QTime
import sqlite3
import re

def validate_pass_number(number):
    if number.isdigit() and 1 <= len(number) <= 10:
        return True
    return False

def validate_name(name):
    if re.match(r'^[a-zA-Zа-яА-Я]+$', name):
        return True
    return False

class TerminalApp(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Оформление пропуска")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.pass_number_label = QLabel("Номер пропуска:")
        self.pass_number_input = QLineEdit()
        self.layout.addWidget(self.pass_number_label)
        self.layout.addWidget(self.pass_number_input)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)

        self.entry_button = QPushButton("Зарегистрировать")
        self.entry_button.clicked.connect(self.register_entry)
        self.layout.addWidget(self.entry_button)

        # self.exit_button = QPushButton("Выход")
        # self.exit_button.clicked.connect(self.register_exit)
        # self.layout.addWidget(self.entry_button)

        self.connection = sqlite3.connect("attendance.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pass_number INTEGER,
                name TEXT,
                surname TEXT,
                entry_time TIMESTAMP,
                exit_time TIMESTAMP
            )
        """)

        self.conn = sqlite3.connect("person_data.db")
        self.cur = self.conn.cursor()

    def register_entry(self):
        number = self.pass_number_input.text().strip()
        first_name = self.name_input.text().strip()
        last_name = self.surname_input.text().strip()
        current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

        if not validate_pass_number(number):
            QMessageBox.critical(self, "Ошибка", "Некорректный номер пропуска")
            return

        if not validate_name(first_name) or not validate_name(last_name):
            QMessageBox.critical(self, "Ошибка", "Некорректное имя или фамилия")
            return

        self.cursor.execute("INSERT INTO employees (pass_number, name, surname, entry_time) VALUES (?, ?, ?, ?)",
                            (number, first_name, last_name, current_time))
        self.connection.commit()

        QMessageBox.information(self, "Успех", "Пропуск успешно зарегистрирован")



        time = QTime.currentTime()
        expiration_time = time.addSecs(2 * 60 * 60)  # 2 часа

        self.cur.execute("INSERT INTO person_data (first_name, last_name, number, expiration_time) VALUES (?, ?, ?, ?)",
                         (first_name, last_name, number, expiration_time.toString(Qt.DateFormat.ISODate)))
        self.conn.commit()

        self.name_input.clear()
        self.surname_input.clear()
        self.pass_number_input.clear()

        QTimer.singleShot(2 * 60 * 60 * 1000, self.delete_person)  # Запустить удаление через 2 часа


    def register_exit(self):

        number = self.pass_number_input.text().strip()
        current_time = QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)

        if not validate_pass_number(number):
            QMessageBox.critical(self, "Ошибка", "Некорректный номер пропуска")
            return

        self.cursor.execute("UPDATE employees SET exit_time = ? WHERE pass_number = ?",
                            (current_time, number))
        self.connection.commit()

        QMessageBox.information(self, "Успех", "Пропуск успешно зарегистрирован")

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

    def delete_person(self):
        current_time = QTime.currentTime().toString(Qt.DateFormat.ISODate)

        self.cur.execute("DELETE FROM person_data WHERE expiration_time <= ?", (current_time,))
        self.conn.commit()

def main():
    app = QApplication(sys.argv)

    terminal_app = TerminalApp()
    terminal_app.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()