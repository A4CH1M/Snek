from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt


class Leaderboard(QDialog):
    """
    Class responsible for creating a leaderboard containing all the saved scores.
    """
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 180)

        self.setObjectName('main')
        self.__layout = QVBoxLayout()

        self.setWindowTitle('LEADERBOARD')
        self.__label = QLabel('HIGHEST SCORES')
        self.__label.setAlignment(Qt.AlignCenter)
        self.__label.setObjectName('highest_scores')

        self.__scores = QLabel('')
        self.__scores.setAlignment(Qt.AlignCenter)
        self.__scores.setObjectName('highest_scores')

        self.__scroll_area = QScrollArea()

        self.__scroll_area.setWidget(self.__scores)
        self.__scroll_area.setWidgetResizable(True)

        self.__exit = QPushButton('GO BACK')
        self.__exit.clicked.connect(self.accept)
        self.__exit.setObjectName('highest_scores')

        self.get_scores_from_file()

        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__scroll_area)
        self.__layout.addWidget(self.__exit)

        self.setLayout(self.__layout)

        self.show()

    def get_scores_from_file(self):
        """
        Method responsible for reading and displaying scores from a file.
        :return: None
        """
        with open('scores.txt', 'r') as scores:
            score_list = []
            for line in scores:
                # score_list.append(line.strip().split(';'))
                nick, points = line.strip().split(';')
                score_list.append((nick, int(points)))

            score_list.sort(key=lambda row: row[1], reverse=True)

            for score in score_list:
                self.__scores.setText(f'{ self.__scores.text() }{ score[0] }: { score[1] }\n')
