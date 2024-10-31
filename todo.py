from PyQt5.QtWidgets import *
from db_connect import get_connection


class AddProductDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Ish qo'shish")
        self.setGeometry(650, 350, 300, 200)
        self.createWidgets()
        self.user_id = user_id

    def createWidgets(self):
        self.form_layout = QFormLayout(self)

        self.todo_name = QLineEdit()

        self.state_combo = QComboBox(self)
        self.state_combo.addItems(["Bajarilgan", "Bajarilmagan"])

        self.form_layout.addRow("Nomi:", self.todo_name)
        self.form_layout.addRow("Holati:", self.state_combo)

        self.save_button = QPushButton("Saqlash")
        self.save_button.clicked.connect(self.save_todo)
        self.form_layout.addRow(self.save_button)

    def save_todo(self):
        a = self.todo_name.text()
        b = self.state_combo.currentText()

        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO todos (user_id,title,status)
            VALUES (%s, %s, %s);
        """
        cursor.execute(query, (self.user_id, a, b))
        connection.commit()
        connection.close()
        QMessageBox.information(self, "Muvaffaqiyat", "Ish muvaffaqiyatli qo'shildi!")
        self.accept()


class ToDo(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Todo ilovasi")
        self.setGeometry(100, 100, 800, 600)
        self.createWidgets()

        self.load_rows()

    def createWidgets(self):
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Id", "Nomi", "Holati", "Date"])
        self.setCentralWidget(self.table_widget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("Amallar")

        add_action = QAction("Qo'shish", self)
        add_action.triggered.connect(self.add_todo)
        file_menu.addAction(add_action)

    def add_todo(self):
        dialog = AddProductDialog(self.user_id)
        dialog.exec_()

        self.load_rows()

    def load_rows(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("Select * from todos where user_id=%s;", (self.user_id,))

        todos = cursor.fetchall()

        self.table_widget.setRowCount(len(todos))

        for index, element in enumerate(todos):
            id = element[0]
            title = element[2]
            state = element[3]
            date = element[4]

            self.table_widget.setItem(index, 0, QTableWidgetItem(id))
            self.table_widget.setItem(index, 1, QTableWidgetItem(title))
            self.table_widget.setItem(index, 2, QTableWidgetItem(state))
            self.table_widget.setItem(
                index, 3, QTableWidgetItem(date.strftime("%d.%m.%Y"))
            )
