from todo import ToDo
from PyQt5.QtWidgets import *
from db_connect import *
import re

import mysql.connector


class RegisterWindow(QWidget):
    regions = [
        "Toshkent shahri",
        "Andijon viloyati",
        "Namangan viloyati",
        "Farg'ona viloyati",
        "Sirdaryo viloyati",
        "Jizzax viloyati",
        "Samarqand viloyati",
        "Navoiy viloyati",
        "Buxoro viloyati",
        "Xorazm viloyati",
        "Qashqadaryo viloyati",
        "Surxondaryo viloyati",
    ]

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ro'yxatdan o'tish")
        self.setGeometry(600, 300, 400, 400)
        self.createWidgets()
        self.show()

    def createWidgets(self):
        self.ism_yozish = QLineEdit(self)
        self.ism_yozish.setPlaceholderText("Ismingizni kiriting")

        self.fam_yozish = QLineEdit(self)
        self.fam_yozish.setPlaceholderText("Familiyangizni kiriting")

        self.age_kiritish = QLineEdit(self)
        self.age_kiritish.setPlaceholderText("Yoshingizni kiriting")

        self.tel_raqam = QLineEdit(self)
        self.tel_raqam.setPlaceholderText("+998 ")

        self.email_kiritish = QLineEdit(self)
        self.email_kiritish.setPlaceholderText("Emailingizni kiriting")

        self.parol_kiritish = QLineEdit(self)
        self.parol_kiritish.setPlaceholderText("Parolingizni kiriting")
        self.parol_kiritish.setEchoMode(QLineEdit.Password)

        self.jins_erkak = QRadioButton("Erkak", self)
        self.jins_ayol = QRadioButton("Ayol", self)

        self.region_combo = QComboBox(self)
        self.region_combo.addItems(self.regions)
        self.saqlash_button = QPushButton("Ro'yxatdan o'tish", self)
        self.saqlash_button.clicked.connect(self.saqla)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ismingiz:"))
        layout.addWidget(self.ism_yozish)
        layout.addWidget(QLabel("Familiyangiz:"))
        layout.addWidget(self.fam_yozish)
        layout.addWidget(QLabel("Yoshingiz:"))
        layout.addWidget(self.age_kiritish)
        layout.addWidget(QLabel("Telefon raqamingiz:"))
        layout.addWidget(self.tel_raqam)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_kiritish)
        layout.addWidget(QLabel("Parol:"))
        layout.addWidget(self.parol_kiritish)

        jins_layout = QHBoxLayout()
        jins_layout.addWidget(self.jins_erkak)
        jins_layout.addWidget(self.jins_ayol)
        layout.addWidget(QLabel("Jinsingiz:"))
        layout.addLayout(jins_layout)

        layout.addWidget(QLabel("Viloyatingiz:"))
        layout.addWidget(self.region_combo)
        layout.addWidget(self.saqlash_button)

        self.setLayout(layout)

    def saqla(self):
        if not self.validate_inputs():
            return

        user_info = {
            "ism": self.ism_yozish.text(),
            "familiya": self.fam_yozish.text(),
            "yosh": int(self.age_kiritish.text()),
            "tel_raqam": self.tel_raqam.text(),
            "email": self.email_kiritish.text(),
            "parol": self.parol_kiritish.text(),
            "jins": "Erkak" if self.jins_erkak.isChecked() else "Ayol",
            "viloyat": self.region_combo.currentText(),
        }

        self.insert_user(user_info)

    def validate_inputs(self):
        if not self.ism_yozish.text():
            self.ism_yozish.setPlaceholderText("Ismingizni kiriting!")
            return False
        if not self.fam_yozish.text():
            self.fam_yozish.setPlaceholderText("Familiyangizni kiriting!")
            return False
        if not self.age_kiritish.text().isdigit():
            self.age_kiritish.setPlaceholderText("Yoshingizni togri kiriting!")
            return False
        if not self.tel_raqam.text()[
            1:
        ].isdigit() or not self.tel_raqam.text().startswith("+998"):
            self.tel_raqam.setPlaceholderText("Telefon raqam notogri!")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email_kiritish.text()):
            self.email_kiritish.setPlaceholderText("Emailni togri kiriting!")
            return False
        if not self.parol_kiritish.text():
            self.parol_kiritish.setPlaceholderText("Parolingizni kiriting!")
            return False
        if not self.jins_erkak.isChecked() and not self.jins_ayol.isChecked():
            QMessageBox.warning(self, "Warning", "Jinsingizni tanlang!")
            return False
        return True

    def insert_user(self, user_info):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO users (ism, familiya, yosh, tel_raqam, email, parol, jins, viloyat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, tuple(user_info.values()))
            connection.commit()
            QMessageBox.information(self, "Success", "Ro'yxatdan o'tdingiz!")
            self.open_login_window()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "Error", f"Ro'yxatdan o'tishda xatolik: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(600, 300, 400, 200)
        self.createWidgets()
        self.show()

    def createWidgets(self):
        default_email = "r@r.com"
        default_password = "@Dev.R789"

        self.email_login = QLineEdit(self)
        self.email_login.setText(default_email)
        self.email_login.setPlaceholderText("Emailingizni kiriting")

        self.parol_login = QLineEdit(self)
        self.parol_login.setText(default_password)
        self.parol_login.setPlaceholderText("Parolingizni kiriting")
        self.parol_login.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Kirish", self)
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_login)
        layout.addWidget(QLabel("Parol:"))
        layout.addWidget(self.parol_login)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        email = self.email_login.text()
        parol = self.parol_login.text()

        connection = get_connection()
        cursor = connection.cursor()
        print("Connection", connection, "Cursor", cursor)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND parol = %s", (email, parol)
        )

        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, "Success", "Tizimga kirdingiz!")
            self.open_todo_window(result[0])
        else:
            QMessageBox.warning(self, "Error", "Email yoki parol xato!")

    def open_todo_window(self, user_id):
        self.todo_window = ToDo(user_id)
        self.todo_window.show()
        self.close()
