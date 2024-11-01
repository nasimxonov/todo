import sys

from register import LoginWindow, RegisterWindow
from PyQt5.QtWidgets import *
from db_connect import create_tables


def main():
    create_tables()

    app = QApplication(sys.argv)
    register_window = RegisterWindow()  
    register_window.show()  
    sys.exit(app.exec_())  

if __name__ == "__main__":
    main()
