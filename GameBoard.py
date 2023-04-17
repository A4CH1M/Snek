from PyQt5.QtWidgets import QWidget, QGridLayout, QDialog
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPainter, QColor
import GameOverWindow as gm
import numpy as np


class GameBoard(QWidget):
    """
    Class creating game board.
    This is responsible fo all actions taken during the game.
    """
    def __init__(self, board_size):
        super().__init__()

        self.__has_eaten = False
        self.__is_apple_collision = False
        self.__has_died = False
        self.__may_click = True
        self.__borderless_mode = False
        self.__light_theme = False
        self.__increased_difficulty = False

        self.__board_size = board_size
        self.__snake_speed = None

        self.setFixedSize(500, 500)
        self.__square_size = 500 // (self.__board_size + 2)

        self.__board_layout = QGridLayout()
        self.__board_grid = None

        self.__current_head_x_coordinate = None
        self.__current_head_y_coordinate = None

        self.__current_tail_end_x_coordinate = None
        self.__current_tail_end_y_coordinate = None

        self.__tail_directions = list()
        self.__snake_direction = None
        self.__snake_tail_size = None

        self.init_game_board()

        self.__show_grid = 1
        self.__obstacle_divider = 5
        self.__obstacle_limiter = 10

        self.__timer = QBasicTimer()

        self.__speed_dict = {
            'BORING': 300,
            'EASY': 200,
            'NORMAL': 100,
            'HARD': 100,
            'INSANE': 50
        }

        self.setLayout(self.__board_layout)

    @property
    def may_click(self):
        return self.__may_click

    @property
    def has_died(self):
        return self.__has_died

    @property
    def snake_tail_size(self):
        return self.__snake_tail_size

    @property
    def snake_direction(self):
        return self.__snake_direction

    @property
    def timer(self):
        return self.__timer

    @may_click.setter
    def may_click(self, value):
        if value:
            self.__may_click = True
        else:
            self.__may_click = False

    @snake_direction.setter
    def snake_direction(self, val):
        if val in [1, 2, 3, 4]:
            self.__snake_direction = val

    @timer.setter
    def timer(self, val):
        self.__timer = val

    def init_game_board(self):
        """
        Initializes game board with parameters (size) provided in the __init__ method
        :return: None
        """
        self.__board_grid = np.zeros((self.__board_size + 2, self.__board_size + 2), dtype=int)
        self.__current_head_x_coordinate = self.__board_size // 2
        self.__current_head_y_coordinate = self.__board_size // 4

        self.__current_tail_end_x_coordinate = self.__current_head_x_coordinate
        self.__current_tail_end_y_coordinate = self.__current_head_y_coordinate - 1
        #    1
        # 4     2
        #    3
        self.__tail_directions.clear()
        self.__tail_directions.append(2)
        self.__snake_direction = 2
        self.__snake_tail_size = 1

        self.__board_grid[self.__current_head_x_coordinate][self.__current_head_y_coordinate] = 1
        self.__board_grid[self.__current_tail_end_x_coordinate][self.__current_tail_end_y_coordinate] = 2
        self.__spawn_first_apple()

        if not self.__borderless_mode:
            for i in range(self.__board_grid.shape[0]):
                for j in range(self.__board_grid.shape[1]):
                    if j == 0 or j == self.__board_size + 1 or i == 0 or i == self.__board_size + 1:
                        self.__board_grid[i][j] = 4

        self.__has_died = False

    def __spawn_first_apple(self):
        """
        Method placing first apple on the board.
        :return:
        """
        while True:
            tmp_x = np.random.randint(1, self.__board_grid.shape[0] - 2)
            tmp_y = np.random.randint(1, self.__board_grid.shape[1] - 2)
            if self.__board_grid[tmp_x][tmp_y] == 0:
                self.__board_grid[tmp_x][tmp_y] = 3
                break

    def start_game(self):
        """
        Starts the timer
        :return: None
        """
        self.__timer.start(self.__snake_speed, self)

    def stop_game(self):
        """
        Stops the timer
        :return: None
        """
        self.__timer.stop()

    def set_map_size(self, size):
        """
        Method sets map size set in settings.
        :param size: Argument taken from settings. Indicates size of the board.
        :return:
        """
        self.__board_size = size
        self.__square_size = 500 // (self.__board_size + 2)
        if self.__board_size < 14:
            self.__obstacle_divider = 7
            self.__obstacle_limiter = 5
        elif self.__board_size < 21:
            self.__obstacle_divider = 5
            self.__obstacle_limiter = 10
        elif self.__board_size < 29:
            self.__obstacle_divider = 3
            self.__obstacle_limiter = 15
        else:
            self.__obstacle_divider = 1
            self.__obstacle_limiter = 20

    def set_grid(self, grid):
        """
        Sets whether to show grid layout.
        :param grid: Argument taken from settings. Boolean variable indicating whether to show grid layout.
        :return: None
        """
        if grid:
            self.__show_grid = 1
        else:
            self.__show_grid = 0

    def set_mode(self, mode):
        """
        Enables/disables borderless mode.
        :param mode: Argument taken from the settings. Boolean variable indicating whether to set mode as borderless.
        :return: None
        """
        self.__borderless_mode = mode

    def set_speed(self, diff_level):
        """
        Sets the speed of the snake and indicates whether to create obstacles
        :param diff_level: Argument taken from the settings.
        :return: None
        """
        self.__snake_speed = self.__speed_dict[diff_level]
        if diff_level == 'INSANE' or diff_level == 'HARD':
            self.__increased_difficulty = True
        else:
            self.__increased_difficulty = False

    def set_theme(self, theme):
        """
        Sets colour theme.
        :param theme: Value taken from the settings. Boolean value.
        :return:
        """
        self.__light_theme = theme

    def move_snake(self):
        """
        Method responsible for setting next coordinates of the snake.
        Updates the tail direction list.
        Checks whether the collision with an apple or an obstacle occurred.
        :return: None
        """
        # dodac nowy kierunek do listy kier

        self.__tail_directions.append(self.__snake_direction)
        # sprawdzic, czy trzeba usunac ostatni element
        if not self.__has_eaten and not self.__borderless_mode:
            # dla koordynatow ostatniego coska ustawic 0
            self.__board_grid[self.__current_tail_end_x_coordinate][self.__current_tail_end_y_coordinate] = 0
            # przesunac koordynaty ostatniego coska w kierunku z listy kier
            if self.__tail_directions[0] == 1:
                self.__current_tail_end_x_coordinate -= 1
            if self.__tail_directions[0] == 2:
                self.__current_tail_end_y_coordinate += 1
            if self.__tail_directions[0] == 3:
                self.__current_tail_end_x_coordinate += 1
            if self.__tail_directions[0] == 4:
                self.__current_tail_end_y_coordinate -= 1
            # usunac pierwszy kierunek z listy kerunkow
            self.__tail_directions.pop(0)

        if not self.__has_eaten and self.__borderless_mode:
            self.__board_grid[self.__current_tail_end_x_coordinate][self.__current_tail_end_y_coordinate] = 0
            # I am not prising such a pitiful attempt -> Bubciu2k is the author here
            # I am not signing below this
            if self.__tail_directions[0] == 1:
                if self.__current_tail_end_x_coordinate == 0:
                    self.__current_tail_end_x_coordinate = self.__board_size + 1
                else:
                    self.__current_tail_end_x_coordinate -= 1

            if self.__tail_directions[0] == 2:
                if self.__current_tail_end_y_coordinate == self.__board_size + 1:
                    self.__current_tail_end_y_coordinate = 0
                else:
                    self.__current_tail_end_y_coordinate += 1

            if self.__tail_directions[0] == 3:
                if self.__current_tail_end_x_coordinate == self.__board_size + 1:
                    self.__current_tail_end_x_coordinate = 0
                else:
                    self.__current_tail_end_x_coordinate += 1

            if self.__tail_directions[0] == 4:
                if self.__current_tail_end_y_coordinate == 0:
                    self.__current_tail_end_y_coordinate = self.__board_size + 1
                else:
                    self.__current_tail_end_y_coordinate -= 1

            self.__tail_directions.pop(0)

        # znalezc head w macierzy i ustawic 2
        self.__board_grid[self.__current_head_x_coordinate][self.__current_head_y_coordinate] = 2
        # ustawic nowe koordynaty glowy bazujac na kierunku i wpisac do macierzy 1

        if not self.__borderless_mode:
            if self.__snake_direction == 1:
                self.__current_head_x_coordinate -= 1

            if self.__snake_direction == 2:
                self.__current_head_y_coordinate += 1

            if self.__snake_direction == 3:
                self.__current_head_x_coordinate += 1

            if self.__snake_direction == 4:
                self.__current_head_y_coordinate -= 1
        else:
            if self.__snake_direction == 1:
                if self.__current_head_x_coordinate == 0:
                    self.__current_head_x_coordinate = self.__board_size + 1
                else:
                    self.__current_head_x_coordinate -= 1

            if self.__snake_direction == 2:
                if self.__current_head_y_coordinate == self.__board_size + 1:
                    self.__current_head_y_coordinate = 0
                else:
                    self.__current_head_y_coordinate += 1

            if self.__snake_direction == 3:
                if self.__current_head_x_coordinate == self.__board_size + 1:
                    self.__current_head_x_coordinate = 0
                else:
                    self.__current_head_x_coordinate += 1

            if self.__snake_direction == 4:
                if self.__current_head_y_coordinate == 0:
                    self.__current_head_y_coordinate = self.__board_size + 1
                else:
                    self.__current_head_y_coordinate -= 1

        next_head_position = self.__board_grid[self.__current_head_x_coordinate][self.__current_head_y_coordinate]

        if next_head_position == 3:
            self.__is_apple_collision = True

        self.__board_grid[self.__current_head_x_coordinate][self.__current_head_y_coordinate] = 1

        if next_head_position == 2 or next_head_position == 4:
            self.__has_died = True
        else:
            self.__has_eaten = False

    def game_over(self):
        """
        Method responsible for displaying a window informing of the ending of the game
        Calls the stop_game() method to stop the timer and clears tail direction list.
        :return: None
        """
        dial = gm.GameOverWindow(self.__snake_tail_size, )
        if dial.exec_() == QDialog.Accepted:
            pass

        self.stop_game()
        self.__tail_directions.clear()
        # self.init_game_board()

    def ate_apple(self):
        """
        Method updates size of the snake's tail.
        Draws coordinates for a new apple.
        :return: None
        """
        self.__snake_tail_size += 1
        self.__has_eaten = True
        while True:
            tmp_x = np.random.randint(1, self.__board_grid.shape[0] - 2)
            tmp_y = np.random.randint(1, self.__board_grid.shape[1] - 2)
            if self.__board_grid[tmp_x][tmp_y] == 0:
                self.__board_grid[tmp_x][tmp_y] = 3
                break

    def generate_obstacles(self):
        """
        Method generates obstacles on the map.
        :return: None
        """
        self.__board_grid[self.__board_grid == 4] = 0
        if not self.__borderless_mode:
            for i in range(self.__board_grid.shape[0]):
                for j in range(self.__board_grid.shape[1]):
                    if j == 0 or j == self.__board_size + 1 or i == 0 or i == self.__board_size + 1:
                        self.__board_grid[i][j] = 4

        num_of_obstacles = self.__snake_tail_size // self.__obstacle_divider + 1

        if num_of_obstacles > self.__obstacle_limiter:
            num_of_obstacles = self.__obstacle_limiter

        for _ in range(num_of_obstacles - 1):
            while True:
                tmp_x = np.random.randint(1, self.__board_grid.shape[0] - 2)
                tmp_y = np.random.randint(1, self.__board_grid.shape[1] - 2)
                if self.__board_grid[tmp_x][tmp_y] == 0:
                    self.__board_grid[tmp_x][tmp_y] = 4
                    break

    def timerEvent(self, event):
        """
        Method calls the method responsible for the snake's movement and checks collisions.
        Updates the GameBoard object.
        :param: event: Timer event
        :return: None
        """
        if event.timerId() == self.__timer.timerId():
            self.move_snake()
            if self.__is_apple_collision:
                self.ate_apple()
                self.__is_apple_collision = False
                if self.__increased_difficulty:
                    self.generate_obstacles()
            if self.__has_died:
                self.game_over()

            self.__may_click = True
            self.update()

    def paintEvent(self, event):
        """
        Calls the method responsible for drawing on the board providing the necessary parameters.
        :return: None
        """
        painter = QPainter(self)
        if self.__light_theme:
            colours = [QColor(0xafe1af),  # field
                       QColor(0x0000ff),  # snake head
                       QColor(0x00ffff),  # snake tail
                       QColor(0xff0000),  # apple
                       QColor(0x6f4e37)]  # block
        else:
            colours = [QColor(0x228b22),  # field
                       QColor(0x00008b),  # snake head
                       QColor(0x00ffff),  # snake tail
                       QColor(0x8b0000),  # apple
                       QColor(0x5c4033)]  # block

        for i in range(self.__board_grid.shape[0]):
            for j in range(self.__board_grid.shape[1]):
                self.draw_square(painter,
                                 self.contentsRect().left() + j * self.__square_size,
                                 self.contentsRect().top() + i * self.__square_size,
                                 colours[self.__board_grid[i][j]])

    def draw_square(self, painter, x, y, colour):
        """
        Method responsible for drawing on the board.
        :param painter: PyQT5.QtGui.QPainter object
        :param x: x coordinate on the NumPy Array
        :param y: y coordinate on the NumPy Array
        :param colour: PyQt5.Qt.QColor object - desired colour
        :return: None
        """
        painter.fillRect(x + 2, y + 2, self.__square_size - self.__show_grid,  self.__square_size - self.__show_grid, colour)

    # def restart(self):
    #     """
    #     Useless thing; No, it's staying
    #     :return: None
    #     """
    #     # if self.timer.isActive():
    #     #     self.init_game_board()
    #     self.start_game()
