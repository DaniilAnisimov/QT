import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import numexpr as ne


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/Graph.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.widget.clear()
        coordinates = [[], []]  # [[x], [y]]
        try:
            # Получаем уравнение
            equation = self.lineEdit.text()
            # Проходимся по заданному диапазону
            for x in range(int(self.le_from.text()), int(self.le_before.text()) + 1):
                # Заменяем в уравнении все вхождения "x" на его числовое значение
                new_equation = equation[:]
                for j in range(new_equation.count("x")):
                    g = new_equation.find("x")
                    new_equation = new_equation[:g] + str(x) + new_equation[g + 1:]
                # Добавляем координаты в список
                coordinates[0].append(x)
                coordinates[1].append(float(ne.evaluate(new_equation)))
            # Начнем выполнять построение
            self.widget.plot(coordinates[0], coordinates[1], pen='r')
        except Exception as E:
            self.statusBar().showMessage(f"Программе не удалось построить данный график.")
            print(E)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
