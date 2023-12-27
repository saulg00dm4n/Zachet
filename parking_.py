import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QMessageBox
import sqlite3


class ParkingApp2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для парковки гостей")
        self.setGeometry(300, 300, 300, 200)

        self.label_guest_id = QLabel("Номер гостя:")
        self.line_edit_guest_id = QLineEdit()
        self.label_parking_spot = QLabel("Номер парковочного места:")
        self.line_edit_parking_spot = QLineEdit()
        self.button_add = QPushButton("Выписать талон")
        self.button_remove = QPushButton("Удалить информацию")

        layout = QVBoxLayout()
        layout.addWidget(self.label_guest_id)
        layout.addWidget(self.line_edit_guest_id)
        layout.addWidget(self.label_parking_spot)
        layout.addWidget(self.line_edit_parking_spot)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_remove)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.button_add.clicked.connect(self.add_parking_ticket)
        self.button_remove.clicked.connect(self.remove_parking_ticket)

        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect("parking.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS guests (pass_number INTEGER PRIMARY KEY, space_number INTEGER)")
        conn.commit()
        conn.close()

    def add_parking_ticket(self):
        guest_id = self.line_edit_guest_id.text()
        parking_spot = self.line_edit_parking_spot.text()

        if guest_id and parking_spot:
            conn = sqlite3.connect("parking.db")
            c = conn.cursor()
            c.execute("INSERT INTO guests (pass_number, space_number) VALUES (?, ?)", (guest_id, parking_spot))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Запись успешно добавлена")

            self.line_edit_guest_id.clear()
            self.line_edit_parking_spot.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните все поля")

    def remove_parking_ticket(self):
        guest_id = self.line_edit_guest_id.text()

        if guest_id:
            conn = sqlite3.connect("parking.db")
            c = conn.cursor()
            c.execute("DELETE FROM guests WHERE pass_number = ?", (guest_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Запись успешно удалена")

            self.line_edit_guest_id.clear()
            self.line_edit_parking_spot.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите номер гостя")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingApp2()
    window.show()
    sys.exit(app.exec())