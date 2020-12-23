from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
import sqlite3
import sys


class addEditCoffeeForm(QMainWindow):
    def __init__(self, parent=None):
        super(addEditCoffeeForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.combo_grind.addItems(["молотый", "в зернах"])
        self.combo_degree_of_roast.addItems(["high", "medium", "low"])
        self.spin_cost.setMaximum(10000)
        self.spin_volume.setMaximum(10000)
        self.mode = 1
        self.pushButton.clicked.connect(self.check)

    def check(self):
        if len(self.line_variety_name.text()):
            variety_name = self.line_variety_name.text()
            degree_of_roast = self.combo_degree_of_roast.currentText()
            grind = self.combo_grind.currentText()
            flavor_description = self.line_flavor_description.text()
            cost = str(self.spin_cost.value())
            volume = str(self.spin_volume.value())
            if self.mode:
                self.parent().add(variety_name, degree_of_roast, grind, flavor_description, cost, volume)
                self.mode = 1
            else:
                self.parent().edit(variety_name, degree_of_roast, grind, flavor_description, cost, volume)
            self.close()
            self.__init__(self.parent())

    def set(self, variety_name, degree_of_roast, grind, flavor_description, cost, volume):
        self.line_variety_name.setText(variety_name)
        self.combo_degree_of_roast.setCurrentIndex(["high", "medium", "low"].index(degree_of_roast))
        self.combo_grind.setCurrentIndex(["молотый", "в зернах"].index(grind))
        self.line_flavor_description.setText(flavor_description)
        self.spin_cost.setValue(float(cost))
        self.spin_volume.setValue(float(volume))
        self.mode = 0


class CoffeeBase(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.loadTable()
        self.add_edit_form = addEditCoffeeForm(self)
        self.currentID = 1

        self.btn_add.clicked.connect(self.open_add_form)
        self.btn_edit.clicked.connect(self.open_edit_form)

    def open_add_form(self):
        self.add_edit_form.show()

    def open_edit_form(self):
        row = list([i.row() for i in self.tableWidget.selectedItems()])
        if not len(row):
            return
        row = [self.tableWidget.item(row[0], i).text() for i in range(self.tableWidget.columnCount())]
        self.currentID = row[0]
        self.add_edit_form.set(*row[1:])
        self.add_edit_form.show()

    def add(self, *parameters):
        req = """INSERT INTO coffee(variety_name, degree_of_roast, grind, flavor_description, cost, volume)
                 VALUES(?,?,?,?,?,?)"""
        cur = self.con.cursor()
        cur.execute(req, parameters)
        self.con.commit()
        self.loadTable()

    def edit(self, *parameters):
        req = """UPDATE coffee
                SET variety_name = ?, degree_of_roast = ?, grind = ?, flavor_description = ?, cost = ?, volume = ?
                WHERE id = ?"""
        cur = self.con.cursor()
        parameters = list(parameters)
        parameters.append(self.currentID)
        cur.execute(req, parameters)
        self.con.commit()
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