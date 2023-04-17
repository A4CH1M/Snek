from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.Qt import Qt


class GameOverWindow(QDialog):
    """
    Class showing on collision allowing to save score.
    """
    def __init__(self, score):
        super().__init__()

        self.__score = score - 1

        self.setFixedSize(320, 180)
        self.setWindowTitle('GAME OVER')

        self.__layout = QVBoxLayout()

        self.__game_over = QLabel('YOU DIED')
        self.__game_over.setAlignment(Qt.AlignCenter)
        self.__score_label = QLabel(f'YOUR SCORE: { str(self.__score) }')
        self.__score_label.setAlignment(Qt.AlignCenter)
        self.__username_text_field = QLineEdit()
        self.__username_text_field.setMaxLength(20)
        self.__username_text_field.setAlignment(Qt.AlignCenter)
        self.__username_text_field.setPlaceholderText('prithee provideth thy nameth'.upper())
        self.__save_score = QPushButton('SAVE YOUR SCORE')
        self.__save_score.clicked.connect(self.save_score_to_file)

        self.__go_back = QPushButton('OK')
        self.__go_back.clicked.connect(self.accept)

        self.__layout.addWidget(self.__game_over, Qt.AlignCenter)
        self.__layout.addWidget(self.__score_label)
        self.__layout.addWidget(self.__username_text_field)
        self.__layout.addWidget(self.__save_score)
        self.__layout.addWidget(self.__go_back)
        self.setLayout(self.__layout)

    def save_score_to_file(self):
        """
        Method responsible for saving a score to a file
        :return: None
        """
        if not self.__username_text_field.text() == '':
            with open('scores.txt', 'a') as scores:
                scores.write(f'{ self.__username_text_field.text() };{ self.__score }\n')

        self.accept()
