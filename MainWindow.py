from PyQt5.QtWidgets import QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QLabel,\
    QPushButton, QDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import Qt, QBasicTimer
import numpy as np
import sys
import GameBoard as gb
import Settings as st
import Leaderboard as lb
import style


class MainWindow(QWidget):
    """
    Class creating the main window and managing the layout of Widgets and other scenes.
    """
    def __init__(self):
        super().__init__()

        self.__scene_manager = QStackedLayout()

        title = 'SNEK'
        width = 960
        height = 540

        if np.random.randint(0, 2) == 1:
            icon_name = r'img\snek_icon.png'
        else:
            icon_name = r'img\snek_icon_but_black.png'

        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(icon_name))
        self.setFixedSize(width, height)

        self.__main_menu = QWidget()
        self.__main_menu_layout = QVBoxLayout()
        self.__main_menu_layout.setAlignment(Qt.AlignCenter)

        self.__title = QLabel(self)
        self.__title.setPixmap(QPixmap(icon_name))
        self.__title.show()
        self.__title.setAlignment(Qt.AlignCenter)

        self.__play_button = QPushButton('PLAY')
        self.__play_button.setFixedSize(300, 40)
        self.__play_button.clicked.connect(self.play_game)

        self.__settings_button = QPushButton('SETTINGS')
        self.__settings_button.setFixedSize(300, 40)
        self.__settings_button.clicked.connect(self.open_settings)

        self.__leaderboard_button = QPushButton('LEADERBOARD')
        self.__leaderboard_button.setFixedSize(300, 40)
        self.__leaderboard_button.clicked.connect(self.show_leaderboard)

        self.__exit_button = QPushButton('EXIT')
        self.__exit_button.setFixedSize(300, 40)
        self.__exit_button.clicked.connect(self.exit_application)

        self.__main_menu_layout.addWidget(self.__title)
        self.__main_menu_layout.addWidget(self.__play_button)
        self.__main_menu_layout.addWidget(self.__settings_button)
        self.__main_menu_layout.addWidget(self.__leaderboard_button)
        self.__main_menu_layout.addWidget(self.__exit_button)

        self.__main_menu.setLayout(self.__main_menu_layout)

        self.__settings = QWidget()
        self.__settings_layout = QVBoxLayout()

        self.__settings_window = st.Settings(self)
        self.__settings_back_to_menu = QPushButton('BACK TO MAIN MENU')
        self.__settings_back_to_menu.setFixedSize(300, 40)

        self.__settings_back_to_menu.clicked.connect(self.back_to_menu_the_sequel)

        self.__settings_layout.addWidget(self.__settings_window)
        self.__settings_layout.addWidget(self.__settings_back_to_menu, alignment=Qt.AlignCenter)
        self.__settings.setLayout(self.__settings_layout)

        self.__game_board = QWidget()

        self.__game_board_layout = QHBoxLayout()
        self.__game_board_window = gb.GameBoard(15)
        self.__game_board_window.set_speed(self.__settings_window.difficulty_level.currentText())

        self.__game_time = QLabel('TIME: 0')
        self.__game_time.setObjectName('stats')
        self.__points = QLabel(f'SCORE: { self.__game_board_window.snake_tail_size - 1}')
        self.__points.setObjectName('stats')

        empty_label_cause_yup = QLabel('-----')
        empty_label_cause_yup.resize(100, 40)

        self.__game_board_pause = QPushButton('PAUSE')
        self.__game_board_pause.setFixedSize(300, 40)
        self.__game_board_pause.clicked.connect(self.pause_game)
        self.__game_board_restart = QPushButton('RESTART')
        self.__game_board_restart.setFixedSize(300, 40)
        self.__game_board_restart.clicked.connect(self.restart)
        self.__game_board_back_to_menu = QPushButton('BACK TO MAIN MENU')
        self.__game_board_back_to_menu.setFixedSize(300, 40)
        self.__game_board_back_to_menu.clicked.connect(self.back_to_menu)

        self.__right = QWidget()
        self.__right_layout = QVBoxLayout()
        self.__right_layout.setAlignment(Qt.AlignCenter)
        self.__right_layout.addWidget(self.__game_time, alignment=Qt.AlignCenter)
        self.__right_layout.addWidget(self.__points, alignment=Qt.AlignCenter)
        self.__right_layout.addWidget(empty_label_cause_yup, alignment=Qt.AlignCenter)
        self.__right_layout.addWidget(self.__game_board_pause)
        self.__right_layout.addWidget(self.__game_board_restart)
        self.__right_layout.addWidget(self.__game_board_back_to_menu)
        self.__right.setLayout(self.__right_layout)

        self.__game_board_layout.addWidget(self.__game_board_window)
        self.__game_board_layout.addWidget(self.__right)

        self.__game_board.setLayout(self.__game_board_layout)

        self.__scene_manager.addWidget(self.__main_menu)
        self.__scene_manager.addWidget(self.__settings)
        self.__scene_manager.addWidget(self.__game_board)
        self.setLayout(self.__scene_manager)

        self.__game_timer = QBasicTimer()
        self.__timer_ticks = 1

        self.setStyleSheet(style.style_default)

        self.__paused = False

        self.show()

    def play_game(self):
        """
        Method responsible for displaying the board and starting the game.
        Changes the scene to the game board, refreshes it if needed and starts the timer.
        :return: None
        """
        self.__game_board_pause.setEnabled(True)
        self.__game_board_pause.setText('PAUSE')
        self.__paused = False

        self.__scene_manager.setCurrentIndex(2)
        if self.__game_board_window.has_died:
            self.__game_board_window.init_game_board()
            self.__game_time.setText(f'TIME: { 0 }')
        self.__game_board_window.start_game()
        self.start_timer()

    def open_settings(self):
        """
        Changes the scene to settings.
        :return: None
        """
        self.__scene_manager.setCurrentIndex(1)

    def back_to_menu(self):
        """
        Changes the scene from game back to main menu
        It pauses the game in the same time
        :return: None
        """
        self.__game_board_window.stop_game()
        self.__game_timer.stop()
        self.__scene_manager.setCurrentIndex(0)

    def back_to_menu_the_sequel(self):
        """
        Changes the scene from settings back to main menu
        Also updates all the settings for the game
        :return: None
        """
        self.back_to_menu()
        self.__game_board_window.set_speed(self.__settings_window.difficulty_level.currentText())
        self.__game_board_window.set_map_size(self.__settings_window.matrix_size.value())
        self.__game_board_window.set_grid(self.__settings_window.show_grid.isChecked())
        self.__game_board_window.set_mode(self.__settings_window.borderless_mode.isChecked())
        self.__game_board_window.set_theme(self.__settings_window.light_theme.isChecked())

        self.__game_time.setText(f'TIME: { 0 }')
        self.__game_board_window.init_game_board()

    @staticmethod
    def exit_application():
        """
        Exits the app
        :return: None
        """
        sys.exit()

    def show_leaderboard(self):
        """
        Opens dialog showcasing saved scores.
        :return: None
        """
        dial = lb.Leaderboard()
        if dial.exec_() == QDialog.Accepted:
            self.do_nothing()

    def do_nothing(self):
        """
        what. the. fuck.
        Don't ask. It's just vibin'. I ain't askin' anymore.
        :return: None
        """
        pass

    def keyPressEvent(self, event):
        """
        Sets snake new direction from keyboard
        This can happen only once per timer tick
        :return: None
        """
        if self.__scene_manager.currentIndex() != 2 or not self.__game_board_window.may_click:
            return
        if event.key() == Qt.Key_W and self.__game_board_window.snake_direction != 3:
            self.__game_board_window.snake_direction = 1
        if event.key() == Qt.Key_D and self.__game_board_window.snake_direction != 4:
            self.__game_board_window.snake_direction = 2
        if event.key() == Qt.Key_S and self.__game_board_window.snake_direction != 1:
            self.__game_board_window.snake_direction = 3
        if event.key() == Qt.Key_A and self.__game_board_window.snake_direction != 2:
            self.__game_board_window.snake_direction = 4
        self.__game_board_window.may_click = False

    def restart(self):
        """
        Resets NumPy array, sets points and time to default and restarts the game.
        :return: None
        """
        self.__game_board_pause.setEnabled(True)
        self.__game_board_pause.setText('PAUSE')
        self.__paused = False
        self.__game_board_window.start_game()
        self.__game_time.setText('TIME: 0')
        self.__points.setText(f'SCORE: { self.__game_board_window.snake_tail_size - 1 }')
        self.__game_board_window.init_game_board()
        self.start_timer()

    def pause_game(self):
        """
        Pauses the game.
        :return: None
        """
        if self.__paused:
            self.start_timer()
            self.__game_board_window.start_game()
            self.__game_board_pause.setText('PAUSE')
            self.__paused = False
        else:
            self.__game_timer.stop()
            self.__game_board_window.stop_game()
            self.__game_board_pause.setText('UNPAUSE')
            self.__paused = True

    def start_timer(self):
        """
        Starts game timer.
        :return: None
        """
        self.__game_timer.start(100, self)

    def timerEvent(self, event):
        """
        Updates in-game time and saves it to a label displayed on the screen.
        :return: None
        """
        if event.timerId() == self.__game_timer.timerId():
            if self.__game_board_window.has_died:
                self.__game_timer.stop()
                self.__game_board_pause.setEnabled(False)

            self.__points.setText(f'SCORE: { self.__game_board_window.snake_tail_size - 1 }')

            if self.__timer_ticks == 10:
                self.__timer_ticks = 0
                time = int(self.__game_time.text()[5:]) + 1
                self.__game_time.setText(f'TIME: { time }')

            self.__timer_ticks += 1
