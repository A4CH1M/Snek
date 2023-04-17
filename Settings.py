import os

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QCheckBox, QSlider, QFormLayout, QSizePolicy
from PyQt5.Qt import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import style


class Settings(QWidget):
    """
    Class creating setting window.
    This is responsible for managing game settings.
    """
    def __init__(self, main_window):
        super().__init__()

        self.__main_window = main_window

        self.__player = QMediaPlayer()

        self.__settings_layout = QFormLayout()

        self.__title = QLabel('SETTINGS')
        self.__title.setAlignment(Qt.AlignCenter)

        self.__label_difficulty_level = QLabel(f'{"DIFFICULTY:": <35}')
        self.__difficulty_level = QComboBox()
        self.__difficulty_level.addItems(['BORING', 'EASY', 'NORMAL', 'HARD', 'INSANE'])
        self.__difficulty_level.setCurrentIndex(1)
        self.__difficulty_level.setFixedSize(300, 30)

        self.__borderless_mode = QCheckBox('BORDERLESS MODE')
        self.__borderless_mode.setChecked(False)

        self.__show_grid = QCheckBox('SHOW GRID')
        self.__show_grid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.__show_grid.setChecked(True)

        self.__matrix_size = QSlider(Qt.Horizontal)
        self.__matrix_size.setMinimum(8)
        self.__matrix_size.setMaximum(33)
        self.__matrix_size.setSingleStep(1)
        self.__matrix_size.setValue(15)
        self.__matrix_size.setTickPosition(QSlider.TicksBelow)
        self.__matrix_size.setTickInterval(1)
        self.__matrix_size.valueChanged.connect(self.update_matrix_size_label)
        self.__label_matrix_size = QLabel(f'MAP SIZE [{ self.__matrix_size.value() }]')

        self.__play_music = QCheckBox('PLAY MUSIC')
        self.__play_music.setChecked(False)
        self.__play_music.stateChanged.connect(self.play_audio_file)

        self.__music_volume = QSlider(Qt.Horizontal)
        self.__music_volume.setMinimum(0)
        self.__music_volume.setMaximum(100)
        self.__music_volume.setSingleStep(1)
        self.__music_volume.setValue(25)
        self.__music_volume.setTickPosition(QSlider.TicksBelow)
        self.__music_volume.setTickInterval(5)
        self.__music_volume.setSingleStep(5)
        self.__music_volume.valueChanged.connect(self.change_volume)
        self.__label_music_volume = QLabel(f'MUSIC VOLUME [{ self.__music_volume.value()}%]')

        self.__theme = QCheckBox('LIGHT THEME')
        self.__theme.setChecked(False)
        self.__theme.stateChanged.connect(self.change_theme)

        self.__settings_layout.addRow(self.__title)
        self.__settings_layout.addRow(self.__label_difficulty_level, self.__difficulty_level)
        self.__settings_layout.addRow(self.__borderless_mode)
        self.__settings_layout.addRow(self.__show_grid)
        self.__settings_layout.addRow(self.__label_matrix_size, self.__matrix_size)
        self.__settings_layout.addRow(self.__play_music)
        self.__settings_layout.addRow(self.__label_music_volume, self.__music_volume)
        self.__settings_layout.addRow(self.__theme)

        self.__settings_layout.setSpacing(30)
        self.setLayout(self.__settings_layout)

        self.__light_theme = False

        self.show()

    @property
    def difficulty_level(self):
        return self.__difficulty_level

    @property
    def show_grid(self):
        return self.__show_grid

    @property
    def borderless_mode(self):
        return self.__borderless_mode

    @property
    def matrix_size(self):
        return self.__matrix_size

    @property
    def play_music(self):
        return self.__play_music

    @property
    def music_volume(self):
        return self.__music_volume

    @property
    def light_theme(self):
        return self.__theme

    def play_audio_file(self):
        """
        Plays/Restarts/Stops music.
        :return: None
        """
        if self.__play_music.isChecked():
            url = QUrl.fromLocalFile(r'music\Undertale_Megalovania.mp3')
            content = QMediaContent(url)

            self.change_volume()

            self.__player.setMedia(content)
            self.__player.play()
        else:
            self.__player.stop()

    def change_volume(self):
        """
        Method changes music volume.
        :return: None
        """
        self.__player.setVolume(self.__music_volume.value())
        self.__label_music_volume.setText(f'MUSIC VOLUME [{ self.__music_volume.value() }%]')

    def update_matrix_size_label(self):
        """
        Updates label.
        :return: None
        """
        self.__label_matrix_size.setText(f'MAP SIZE [{self.__matrix_size.value()}]')

    def change_theme(self):
        """
        Changes colour theme.
        :return: None
        """
        style_sheet = None
        if self.__light_theme:
            style_sheet = style.style_default
            self.__light_theme = False
        else:
            style_sheet = style.style_light
            self.__light_theme = True

        self.__main_window.setStyleSheet(style_sheet)
