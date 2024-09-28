"""Игра змейка."""

from random import choice, randrange
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета, используемые в игре:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

CENTER_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

SPEED = 10

# Словарь для обработки нажатий пользователя и изменения движения
CHANGE_MOVEMENT = {
    (LEFT, pygame.K_UP): UP,
    (RIGHT, pygame.K_UP): UP,
    (UP, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_LEFT): LEFT,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_RIGHT): RIGHT,
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """
    Родительский класс всех объектов в игре.

    Атрибуты
    --------
    position : tuple(int, int)
        Позиция объекта (по умолчанию - CENTER_SCREEN)
    body_color : tuple(int, int, int)
        Цвет объекта (по умолчанию - BOARD_BACKGROUND_SCREEN)

    Методы
    ------
    draw_cell(position, color=None):
        Отрисовка одной ячейки на поле.
    draw():
        Полная отрисовка объекта (переопределён в дочерних классах).
    """

    def __init__(
            self,
            position=CENTER_SCREEN,
            body_color=BOARD_BACKGROUND_COLOR
    ):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """
        Отрисовка одной ячейки на поле.

        Если аргумент 'color' передан, то происходит закрашивание ячейки
        с выделением границ.

        Параметры
        ---------
        position : tuple(int, int)
            Координаты ячейки, которую нужно закрасить
        color: tuple(int, int, int)
            Цвет, которым нужно закрасить ячейку

        Возвращаемое значение
        ---------------------
        None
        """
        if not color:
            color = self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """
        Полная отрисовка объекта.

        Метод переопределён в дочерних классах.
        В случае, если метод вызван для родительского класса,
        генерирует ошибку NotImplementedError.

        Возвращаемое значение
        ---------------------
        None
        """
        raise NotImplementedError(
            f'Вызов пустого метода draw класса {self.__class__.__name__}.'
        )


class Apple(GameObject):
    """
    Класс, описывающий объект 'яблоко' в игре.

    Атрибуты
    --------
    position : tuple(int, int)
        позиция яблока (по умолчанию - CENTER_SCREEN)
    body_color : tuple(int, int, int)
        цвет яблока (по умолчанию - APPLE_COLOR)

    Методы
    ------
    generate_new_poisition(self, occupied_positions):
        Генерация новых координат яблока.
        Для использования вне класса.
    draw():
        Отрисовка яблока на поле.
    _randomize_position(self, occupied_positions):
        Приватный метод генерации новых координат яблока
        с учётом занятых позиций в игре.
    """

    def __init__(
            self,
            occupied_positions=None,
            position=CENTER_SCREEN,
            body_color=APPLE_COLOR
    ):
        super().__init__(position, body_color)
        if not occupied_positions:
            occupied_positions = [CENTER_SCREEN]
        self._randomize_position(occupied_positions)

    def generate_new_poisition(self, occupied_positions):
        """
        Генерация новых координат яблока.
        Для использования вне класса.

        Параметры
        ---------
        occupied_positions : list
            Занятые координаты, на которые нельзя генерировать яблоко

        Возвращаемое значение
        ---------------------
        None
        """
        self._randomize_position(occupied_positions)

    def draw(self):
        """
        Отрисовка яблока на поле

        Возвращаемое значение
        ---------------------
        None
        """
        self.draw_cell(self.position)

    def _randomize_position(self, occupied_positions):
        while self.position in occupied_positions:
            self.position = (
                randrange(0, SCREEN_WIDTH - GRID_SIZE + 1, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT - GRID_SIZE + 1, GRID_SIZE)
            )

    def randomize_position(self):
        """Метод добавлен для прохождения автоматических тестов"""
        pass


class Snake(GameObject):
    """
    Класс, описывающий объект 'змейка' в игре.

    Атрибуты
    --------
    length: int
        длина змейки (по умолчанию length = 1)
    direction: tuple(int, int)
        текущее направление движения змейки (по умолчанию - RIGHT)
    last: tuple(int, int)
        координаты хвоста змейки (по умолчанию - None)
    positions: list
        список координат всей змейки (по умолчанию - [CENTER_SCREEN])
    body_color: tuple(int, int, int)
        цвет змейки (по умолчанию - SNAKE_COLOR)

    Методы
    ------
    update_direction(self, next_direction):
        Обновление движения змейки.
    move():
        Движение змейки.
    draw():
        Отрисовка змейки.
    increase_length_snake():
        Увеличение длины змейки на 1 (в случае съедания яблока).
    get_head_position():
        Метод возвращает координаты головы змейки.
    check_crush():
        Проверка столкновения змейки самой с собой.
    reset():
        Сброс змейки до первоначального состояния.
    """

    def __init__(self, position=CENTER_SCREEN, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT

    def update_direction(self, next_direction):
        """
        Обновление движения змейки.

        Параметры
        ---------
        next_direction: tuple(int, int)
            Направление, на которое нужно сменить текущее

        Возвращаемое значение
        ---------------------
        None
        """
        self.direction = next_direction

    def move(self):
        """
        Движение змейки.

        При выходе змейки за границы поля,
        она появляется с противоположной стороны (оператор %).
        При съедании яблока змейкой, её последний элемент не удаляется.

        Возвращаемое значение
        ---------------------
        None
        """
        dx = self.direction[0] * GRID_SIZE
        dy = self.direction[1] * GRID_SIZE
        new_head_x = (self.get_head_position()[0] + dx) % SCREEN_WIDTH
        new_head_y = (self.get_head_position()[1] + dy) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """
        Отрисовка змейки.

        Возвращаемое значение
        ---------------------
        None
        """
        # Отрисовка головы змеи
        self.draw_cell(self.get_head_position())
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def increase_length_snake(self):
        """
        Увеличение длины змейки на 1 (в случае съедания яблока).

        Возвращаемое значение
        ---------------------
        None
        """
        self.length += 1

    def get_head_position(self):
        """
        Метод возвращает координаты головы змейки

        Возвращаемое значение
        ---------------------
        tuple(int, int)
        """
        return self.positions[0]

    def check_crush(self):
        """
        Проверка столкновения змейки самой с собой.

        Возвращаемое значение
        ---------------------
        bool
        """
        return self.get_head_position() in self.positions[1:]

    def reset(self):
        """
        Сброс змейки до первоначального состояния.

        Возвращаемое значение
        ---------------------
        None
        """
        self.length = 1
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.last = None
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR


def handle_keys(game_object):
    """
    Обрабатывает нажатия пользователя на клавиши.

    Параметры:
        game_object (Snake): змейка
    Возвращаемое значение:
        None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            game_object.update_direction(
                CHANGE_MOVEMENT.get((game_object.direction, event.key),
                                    game_object.direction)
            )


def main():
    """
    Основная функция с логикой игры.

    Возвращаемое значение:
        None
    """
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.check_crush():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif snake.get_head_position() == apple.position:
            snake.increase_length_snake()
            apple.generate_new_poisition(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
