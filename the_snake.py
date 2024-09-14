"""
Игра змейка.

Дорогой ревьюер, пожалуйста, докопайся до моего кода на максимум :)
Чтобы абсолютно все косяки и недочёты были помечены.
Просто я хочу, чтобы мой код максимально профессионально выглядел
и готов всё для этого сделать!!!
+ в будущем собираюсь дополнить код несвежими фруктами и препятствиями.
"""

from random import randrange, choice

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс всех объектов в игре."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод отрисовки объекта на поле,
        переопределён в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс, описывающий объект 'яблоко' на поле.
    При съедании яблока змейкой, её длина увеличивается на 1 клетку.
    """

    def __init__(self):
        super().__init__(self.randomize_position(), (255, 0, 0))

    def draw(self):
        """Метод отрисовки яблока на поле в графическом интерфейсе."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def erase_apple(self):
        """Метод стирания яблока с поля в графическом интерфейсе."""
        apple_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, apple_rect)

    def generate_new_apple(self):
        """Метод создания координат нового яблока (при съедании старого)."""
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position():
        """Метод генерации случайной позиции яблока с учётом размера клеток."""
        pos_x = randrange(0, SCREEN_WIDTH - GRID_SIZE + 1, GRID_SIZE)
        pos_y = randrange(0, SCREEN_HEIGHT - GRID_SIZE + 1, GRID_SIZE)
        return (pos_x, pos_y)


class Snake(GameObject):
    """Класс. описывающий объект 'змейка' на поле."""

    def __init__(self):
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(
            [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)], (0, 255, 0)
        )

    def update_direction(self):
        """
        Метод, изменяющий направление движения змейки
        после нажатия клавиши на клавиатуре.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод совершения движения змейкой
        и проверкой на выход за границы поля (оператор %).
        При съедании яблока змейкой, её последний элемент не удаляется,
        увеличивая длину змейки на 1.
        """
        dx = self.direction[0] * GRID_SIZE
        dy = self.direction[1] * GRID_SIZE
        new_head_x = (self.get_head_position()[0] + dx) % SCREEN_WIDTH
        new_head_y = (self.get_head_position()[1] + dy) % SCREEN_HEIGHT
        self.position.insert(0, (new_head_x, new_head_y))
        if len(self.position) > self.length:
            self.last = self.position[-1]
            self.position.pop()

    def draw(self):
        """Метод отрисовки змейки в интерфейсе с учётом движения."""
        for position in self.position[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def increase_length_snake(self):
        """Метод увеличения длины змейки при съедании яблока."""
        self.length += 1

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.position[0]

    def check_crush(self):
        """
        Метод проверки столкновения змейки с собой.
        В случае столкновения, игра перезапускается.
        """
        return self.get_head_position() in self.position[1:]

    def reset(self):
        """
        Метод перезапуска змейки в случае столкновения.
        Вызывает конструктор и выбирает случайное направление.
        """
        self.__init__()
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


def handle_keys(game_object):
    """Метод обработки нажатия клавиши на клавиатуре"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция main с логикой игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.check_crush():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.increase_length_snake()
            apple.erase_apple()
            apple.generate_new_apple()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
