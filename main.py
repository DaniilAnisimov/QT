import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import Qt

# Номера клавиш с f1 до f12
f = [16777264, 16777265, 16777266, 16777267, 16777268, 16777269,
     16777270, 16777271, 16777272, 16777273, 16777274, 16777275]
# Цифры от 0 до 9 + английский алфавит от A до Z
a = [49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 1049, 1062, 1059,
     1050, 1045, 1053, 1043, 1064, 1065, 1047, 1060, 1067, 1042,
     1040, 1055, 1056, 1054, 1051, 1044, 1071, 1063, 1057, 1052,
     1048, 1058, 1068]
# Доп. кнопки (Ctrl, Alt, Enter, Backspace)
d = [16777249, 16777251, 16777220, 16777219]


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 150, 1040, 150)
        self.setWindowTitle('Фортепиано')
        self.keys = {}
        self.path = "data"  # Каталог в котором лежат звуки клавиш
        self.b_buttons = {}
        self.w_buttons = {}
        self.initUI()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ShiftModifier:
            if event.key() in a:
                self.keys[self.b_buttons[event.key()]][0].play()
        elif event.key() in f + a + d:
            self.keys[self.w_buttons[event.key()]][0].play()

    def initUI(self):
        # Звуки клавиш скачивал последовательно с сайта http://theremin.music.uiowa.edu/MISpiano.html
        files = [os.path.join(self.path, file) for file in os.listdir(self.path)]
        # Сортируем список по дате изменения
        files.sort(key=os.path.getmtime)
        white_keys = []
        black_keys = []
        position = 0
        ib, iw = 0, 0
        w = f + a + d  # Список номеров кнопок доступных для белых клавиш
        b = a          # Для чёрных клавиш
        # Для каждой ноты находим расположение клавиши и её тип
        for way in files:
            name = way[way.find("_ff_") + 4:way.find(".")]
            if len(name) == 3:  # Чёрная клавиша
                black_keys.append([way, name, position - 5])
                self.b_buttons[b[ib]] = name
                ib += 1
            else:  # Белая
                white_keys.append([way, name, position])
                position += 20
                self.w_buttons[w[iw]] = name
                iw += 1
        # Сначала добавляем белые клавиши
        for key in white_keys:
            self.add(*key)
        # Потом чёрные
        for key in black_keys:
            self.add(*key)

    # Функция принимает на вход параметры:
    # way - путь до звука клавиши
    # name - её краткое имя
    # position - координата x (место, где на главном окне будет располагаться клавиша)
    def add(self, way, name, position):
        media = QtCore.QUrl.fromLocalFile(way)
        content = QtMultimedia.QMediaContent(media)
        self.keys[name] = [None, None]
        self.keys[name][0] = QtMultimedia.QMediaPlayer()
        self.keys[name][0].setMedia(content)

        btn = QPushButton('', self)
        if len(name) == 3:
            btn.setStyleSheet('background: rgb(0,0,0);')
            btn.resize(10, 100)
        else:
            btn.setStyleSheet('background: rgb(255,255,255);')
            btn.resize(20, 150)
        btn.move(position, 0)

        self.keys[name][1] = btn
        self.keys[name][1].clicked.connect(self.keys[name][0].play)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
