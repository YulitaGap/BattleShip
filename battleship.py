import random
from random import randint


class Game:
    def __init__(self):
        """
        Initialization of class Game
        (fields : list of fields)
        (players: list of players)
        """
        self.__fields = []
        self.__players = []
        self.__current_player = 0

    @staticmethod
    def shoot_at(cell, field_given):
        """
        Return True if there is a ship in a cell, false if it's empty cell.
        Changes cell position in grid(list) and board(dict).
        (tuple, class) - > boolean
        """
        line = 'abcdefghijklmnopqrstuvwxyz'.index(cell[0].lower())
        field_given.grid[line][cell[1] - 1] = 'X'
        if field_given.board[cell] == 0:
            print('You missed!')
            print(field_given.field_with_ships())
            return False
        elif field_given.board[cell] == 1:
            field_given.grid[line][cell[1] - 1] = '*'
            print('You shoot at ship!')
            field_given.field_with_ships()
            return True
        elif field_given.board[cell] == 'X':
            field_given.field_with_ships()
            return False
        field_given.board[cell] = 'X'

    def board_dict(self):
        """
        Converts a grid to a dictionary type.
        Initializes board attribute.
        (class) -> None
        """
        board_dict = {}
        line_number = 1
        for x in self.grid:
            board_dict[line_number] = [cell.replace('_', '0') for cell in x]
            line_number += 1
        cells = dict()
        letters = [chr(x) for x in range(65, 75)]
        for key, value in board_dict.items():
            for x in range(0, 10):
                cells[letters[x], key] = value[x]
        self.board = cells

    def field_without_ships(self):
        grid = []
        for row in range(10):
            row = []
            for col in range(10):
                row.append('_')
            grid.append(row)
        self.grid = grid


class Field(Game):

    def __init__(self):
        self._ships = []

    def random_row(board):
        return randint(0, len(board) - 1)

    def random_col(board):
        return randint(0, len(board[0]) - 1)

    def random_field(self):
        decks = []
        ships = [(1, 4), (2, 3), (3, 2), (4, 1)]
        for ship in ships:
            for k in range(ship[0]):
                a = random.randint(0, 9)
                x = chr(65+a)
                y = random.randint(1, 10 - ship[1])
                horizontal = random.randint(0, 1)
                deck = Ship((x, y), horizontal)
                if horizontal:
                    deck.length = (1, ship[1])
                else:
                    deck.length = (ship[1], 1)
                decks.append(deck)
        self._ships = decks
        for ship in decks:
            self.board[ship.bow] = 1
            if horizontal:
                for i in range(1, max(ship.length)):
                    self.board[ship.bow[0], ship.bow[1]+i] = 1
            else:
                for i in range(max(ship.length)):
                    self.board[chr(65+i), ship.bow[1]] = 1

    def field_with_ships(self):
        numbers = '123456789'
        print('  | ' + ' | '.join(numbers) + ' |'+' 10 |')
        for number, row in enumerate(self.grid):
            print(chr(65+number), '| ' + ' | '.join(row) + ' |')
        return '\n'


class Ship(Field):
    def __init__(self, bow, horizontal):
        self.bow = bow
        self.horizontal = horizontal
        self.length = ()
        self.hit = []


class Player(Game):
    def __init__(self):
        """
        Initialization of Player class
        """
        self.__name = ''

    def get_name(self):
        self.name = str(input('> Enter your name of nickname: '))
        return self.name

    @staticmethod
    def read_position():
        """
        Get coordinates of cell and return in tuple format
        -> tuple
        """
        try:
            guess_row = str(input(" > Enter Row Letter:")).upper()
            guess_col = int(input(" > Enter Col Number:"))
            cell = (guess_row, guess_col)
            return cell
        except ValueError:
            print('Enter only upper letters and int!')
        except TypeError:
            print('Enter only upper letters and int!')


if __name__ == '__main__':

    print('Game Battleship')
    print('Hello, Player 1!')
    player1 = Player()
    player1.get_name()
    print(player1.name + "'s" ' starting field:')

    game = Game()
    game.current_player = 1
    field1 = Field()
    field1.field_without_ships()
    field1.board_dict()
    field1.field_with_ships()
    print('Now adding ships to your field...')
    field1.random_field()

    print('\n')

    print('Hello, Player 2!')
    player2 = Player()
    player2.get_name()
    print(player2.name + "'s" ' field:')
    game.current_player = 2

    field2 = Field()
    field2.field_without_ships()
    field2.board_dict()
    field2.field_with_ships()
    print('Now adding ships to your field...')
    field2.random_field()
    game._players = [player1, player2]
    game._fields = [field1, field2]
    game.current_player = 0
    field = field2

    def count_unhit(fields):
        """
        Return amount of cells, which are not hit.
        (class Field) - > int
        """
        un_hit = 0
        for key, value in fields.board:
            if type(value) == int:
                un_hit += value
        return un_hit

    while count_unhit(field1) and count_unhit(field2):
        miss = True
        while miss:
            print(game._players[game.current_player].name, ' your turn!')
            point = game._players[game.current_player].read_position()
            if game.shoot_at(point, field) is True:
                game.current_player = 0
                print(game._players[game.current_player].name, ' try again!')
                miss = True
                continue
            else:
                field = field1
                field2.field_with_ships()
                game.current_player = 1
                print(game._players[game.current_player].name, ' your turn!')
                point = game._players[game.current_player].read_position()
                if game.shoot_at(point, field) is True:
                    game.current_player = 1
                    print(game._players[game.current_player].name, ' try again!')
                    # print(game._players[game.current_player].name, ' your turn!')
                    field = field1
                    game.current_player = 1
                    continue
                else:
                    field1.field_with_ships()
                    game.current_player = 0
                    miss = False
                    field = field2
                    continue
    winner = game.current_player
    print('Congratulations, {}, you won!'.format(winner))