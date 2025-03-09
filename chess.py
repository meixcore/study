from abc import ABC, abstractmethod
import doctest

class ChessPiece(ABC):
    """
    Абстрактный класс для шахматных фигур
    """

    def __init__(self, color: str, name: str | None) -> None:
        """
        Параметры для всех шахматных фигур

        :param color: цвет фигуры
        :param name: str, имя фигуры
        """
        self.color: str = color
        self.name: str | None = name

    @abstractmethod
    def get_possible_moves(self) -> list[tuple[int, int]] | None:
        pass

    def __str__(self) -> str:
        """
        Возвращает строковое предствление о фигуре

        :return: str, первая буква фигуры и первая буква цвета (напр. 'PB')
        """

        return f'{self.name}{self.color}'

    def __repr__(self) -> str:
        return self.__str__()

class Pawn(ChessPiece):
    def __init__(self, color: str, name: str | None) -> None:
        """
        Создание и подготовка к работе объекта класса пешка

        :param color: str, цвет фигуры
        :param name: str, имя фигуры
        """
        super().__init__(color, name)

    def get_possible_moves(self) -> list[tuple[int, int]] | None:
        """
        Находим возможные ходы для пешки

        :return: list, список возможных ходов
        """

        if self.color == "W":
            return [(-1, 0), (-1, -1), (-1, 1)]
        elif self.color == "B":
            return [(1, 0), (1, -1), (1, 1)]
        else:
            raise ValueError('Ходы могут быть только для белых или черных фигур')


class Rook(ChessPiece):
    def __init__(self, color: str, name: str) -> None:
        """
        Создание и подготовка к работе объекта класса ладья

        :param color: str, цвет фигуры
        :param name: str, первая буква фигуры
        """
        super().__init__(color, name)

    def get_possible_moves(self) -> list[tuple[int, int]] | None:
        """
        Находим возможные ходы для ладьи

        :return: list, список возможных ходов ладьи
        """

        return [(0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]

class Bishop(ChessPiece):
    def __init__(self, color: str, name: str) -> None:
        """
         Создание и подготовка к работе объекта класса слон

         :param color: str, цвет фигуры
         """
        super().__init__(color, name)

    def get_possible_moves(self) -> list[tuple[int, int]] | None:
        """
        Находим возможные ходы для слона

        :return: list, список возможных ходов слона
        """

        return [(-1, 1), (1, 1), (-1, -1), (1, -1)]

# pawn1 = Pawn('B')
# rook1 = Rook('B')
# bishop1 = Bishop('W')

# print(pawn1.get_possible_moves())
# print(rook1.get_possible_moves())
# print(bishop1.get_possible_moves())
# print(bishop1.__str__())


class ChessBoard:
    """
    Класс представляющий шахматную доску для размещения шахматных фигур
    """
    def __init__(self) -> None:
        """
        Создание и подготовка к работе объекта класса шахматная доска
        """
        self.__empty_cell = ".."
        self.__size = 8
        self.board: list[list[str | ChessPiece]] = [[self.__empty_cell for _ in range(self.__size)] for _ in range(self.__size)]
        self.letters = '   a  b  c  d  e  f  g  h'

    def show_board(self) -> None:
        """
        Отрисовываем шахматную доску и заполняем пустыми символами
        :return: list[list[str | ChessPiece]], проекция шахматной доски
        """
        print(self.letters)
        for i, line in enumerate(self.board):
            print(i, *line)
        print()

    def move_figure(self, start_line: int, start_column: int, target_line: int, target_column: int) -> None:
        """
        После проверок двигаем фигуру из начальной точки в конечную

        :param start_line: int, строка, где находится фигура
        :param start_column: int, столбец, где находится фигура
        :param target_line: int, строка, куда хотим передвинуть фигуру
        :param target_column: int, стобец, куда хотим передвинуть фигуру
        :return: None
        """
        self.__validate_cords(start_line, start_column, target_line, target_column)
        self.__figure_is_real(start_line, start_column)
        self.__move(start_line, start_column, target_line, target_column)

    def __validate_cords(self, start_line: int, start_column: int, target_line: int, target_column: int) -> None:
        """
        Проверяем валидны ли кардинаты, то есть находятся ли они в зоне шахматной доски
        Вызывает исключение ValueError, если координаты находятся вне доски

        :param start_line: int, строка, где находится фигура
        :param start_column: int, столбец, где находится фигура
        :param target_line: int, строка, куда хотим передвинуть фигуру
        :param target_column: int, стобец, куда хотим передвинуть фигуру
        :raise ValueError: Неверные координаты
        :return: None

        # >>> board_test = ChessBoard()
        # >>> board_test.fill_start_board()
        # >>> board_test.move_figure(1, 0, 2, 0)
        #
        # >>> board_test = ChessBoard()
        # >>> board_test.fill_start_board()
        # >>> board_test.move_figure(9, 0, 9, 0)
        # Traceback (most recent call last):
        # ...
        # ValueError: Неверные координаты: (9, 0, 9, 0)
        """

        for c in (start_line, start_column, target_line, target_column):
            if self.__size <= c and 0 <= c:
                raise ValueError(f'Неверные координаты: {(start_line, start_column, target_line, target_column)}')

    def __figure_is_real(self, start_line: int, start_column: int) -> None:
        """
        Проверяем есть ли фигура в начальной точке
        Вызывает исключение ValueError, если на начальных координатах нет фигуры

        :param start_line: int, строка, где находится фигура
        :param start_column: int, столбец, где находится фигура
        :raise ValueError: На указанных координатах ({start_line, start_column}) нет фигуры
        :return: None
        """
        if self.board[start_line][start_column] == self.__empty_cell:
            raise ValueError(f'На указанных координатах ({start_line, start_column}) нет фигуры')

    def __move(self, start_line: int, start_column: int, target_line: int, target_column: int) -> None:
        """
        Процесс перемещения фигуры, в начальной точке теперь будет пустая клетка, в конечной новая фигура
        Вызывает исключение ValueError, если мы пытаемся переместить фигуру на место дружеской фигуры

        :param start_line: int, строка, где находится фигура
        :param start_column: int, столбец, где находится фигура
        :param target_line: int, строка, куда хотим передвинуть фигуру
        :param target_column: int, стобец, куда хотим передвинуть фигуру
        :raise ValueError: Ход невозможен тк стоит френдли фигура
        :return: None
        """

        possible_moves: list[tuple[int, int]] | None = []
        if isinstance(self.board[start_line][start_column], Pawn) and self.board[target_line][target_column] != self.__empty_cell:
            if self.board[start_line][start_column].color == "W":
                possible_moves = [(-1, -1), (-1, 1)]
            elif self.board[start_line][start_column].color == "B":
                possible_moves = [(1, -1), (1, 1)]
        elif isinstance(self.board[start_line][start_column], Pawn) and self.board[target_line][target_column] == self.__empty_cell:
            if self.board[start_line][start_column].color == "W":
                possible_moves = [(-1, 0)]
            elif self.board[start_line][start_column].color == "B":
                possible_moves = [(1, 0)]
        else:
            possible_moves: list[tuple[int, int]] | None = self.board[start_line][start_column].get_possible_moves()

        delta = target_line - start_line, target_column - start_column
        print(
            f'\nХотим переместиться относительно текущих координат фигуры на: {delta}\n'
            f'Доступны для перемещения, относительно текущих координат: {possible_moves}\n'
        )
        if delta in possible_moves:
            if self.board[target_line][target_column] == self.__empty_cell or self.board[start_line][start_column].color != self.board[target_line][target_column].color:
                self.board[target_line][target_column] = self.board[start_line][start_column]
                self.board[start_line][start_column] = self.__empty_cell
            elif self.board[start_line][start_column].color == self.board[target_line][target_column].color:
                raise ValueError(f'Ход невозможен тк стоит френдли фигура')
        else:
            raise ValueError(f'Конечные кординаты вне доступных')


    def fill_start_board(self) -> None:
        """
        Заполняем пустую доску шахматными фигурами, то есть позиция фигур в начале игры

        :return: list[list[str | ChessPiece]]
        """
        self.board[1] = [Pawn(color="B", name='P') for _ in range(self.__size)]
        self.board[6] = [Pawn(color="W", name='P') for _ in range(self.__size)]
        self.board[7][0] = Rook(color='W', name='R')
        self.board[7][7] = Rook(color='W', name='R')
        self.board[0][0] = Rook(color='B', name='R')
        self.board[0][7] = Rook(color='B', name='R')
        self.board[7][2] = Bishop(color='W', name='B')
        self.board[7][5] = Bishop(color='W', name='B')
        self.board[0][2] = Bishop(color='B', name='B')
        self.board[0][5] = Bishop(color='B', name='B')

def get_col(m: str) -> int:
    """
    Метод для соотношения столбца с координатой для дальнейших передвижений фигуры

    :param m: str | int, передаем букву столбца, а получаем его цифру
    :return: int, координата для передвижения фигуры
    """
    letter_to_index = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3,
        'e': 4, 'f': 5, 'g': 6, 'h': 7
    }
    while True:
        if m in letter_to_index:
            return int(letter_to_index[m])
        else:
            raise ValueError(f'буквы {m} нет в названиях столбцов')

# doctest.testmod()

def game():
    c1 = ChessBoard()
    c1.fill_start_board()

    menu = {
        '1': 'Переместить фигуру',
        '0': 'Выйти из игры'
    }
    while True:
        c1.show_board()
        print(menu)
        action = input('Выберите действие: ')

        if action == '1':
            # cords = [
            #     int(x) for x in input("Введите через пробел координаты: start_x, start_y, target_x, target_y ").split()
            # ]
            cor_start_line = int(input('start_line (цифра): '))
            cor_start_col = get_col(input('start_col (буква): ').lower())
            cor_target_line = int(input('target_line (цифра): '))
            cor_target_col = get_col(input('target_col (буква): ').lower())
            c1.move_figure(cor_start_line, cor_start_col, cor_target_line, cor_target_col)
        elif action == '0':
            break

        c1.show_board()

game()