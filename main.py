from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sqlite3
import sys


class CoffeeBase(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.loadTable()

    def loadTable(self):
        req_ALL = """SELECT * FROM coffee"""
        cur = self.con.cursor()
        all_ = cur.execute(req_ALL).fetchall()
        if len(all_):
            self.tableWidget.setColumnCount(len(all_[0]))
        titles = [description[0] for description in cur.description]
        self.tableWidget.setColumnCount(len(titles))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(all_):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeBase()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())