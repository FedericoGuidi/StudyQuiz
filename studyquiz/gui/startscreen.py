from PyQt5.QtWidgets import *

class StartScreen(QWidget):
    def __init__(self) -> None:
        app = QApplication([])
        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('StudyQuiz'))
        layout.addWidget(QPushButton('Start!'))
        window.setLayout(layout)
        window.show()
        app.exec_()
        