"""
Im gonna simulate this game so I can see every way to solve it.
"""

import sys

DEBUG = 0
BOARD_HEIGHT = 5

class Board:
    def __init__(self):
        self.board = self.create_board()
        print(self)

    def create_board(self):
        """
            0 1 2 3 4
            / / / / /
    0 -----x / / / /
    1 ----x x / / /
    2 ---x x x / /
    3 --x x x x /
    4 -x x o x x
        """
        board = [[]] * BOARD_HEIGHT
        for i, _ in enumerate(board):
            board[i] = [1] * (i + 1)

        # Starting empty piece
        board[BOARD_HEIGHT - 1][int((BOARD_HEIGHT - 1) / 2)] = 0
        return board

    def possible_moves(self):
        ret = []
        for i, row in enumerate(self.board):
            for j, _ in enumerate(row):
                this_pos = Position(i, j)
                surr_positions = this_pos.positions_around()
                for surr_pos in surr_positions:
                    jump_pos = this_pos.jump_position(surr_pos)
                    if jump_pos:
                        if not self.piece_at_position(jump_pos) and \
                                self.piece_at_position(surr_pos) and \
                                self.piece_at_position(this_pos):
                            # print("This piece can jump", surr_pos)
                            ret.append(Move(this_pos, surr_pos, jump_pos))
        return ret

    def piece_at_position(self, pos):
        return self.board[pos.x][pos.y]

    def apply_move(self, move):
        self.board[move.pos_from.x][move.pos_from.y] = 0
        self.board[move.pos_over.x][move.pos_over.y] = 0
        self.board[move.pos_to.x][move.pos_to.y] = 1

    def backup_move(self, move):
        self.board[move.pos_from.x][move.pos_from.y] = 1
        self.board[move.pos_over.x][move.pos_over.y] = 1
        self.board[move.pos_to.x][move.pos_to.y] = 0

    def piece_count(self):
        ret = 0
        for row in self.board:
            ret += sum(row)
        return ret


    def __repr__(self):
        ret = ""
        for i, row in enumerate(self.board):
            # add spaces
            ret += " " * (BOARD_HEIGHT - 1 - i)
            # add pieces
            ret += " ".join(map(str, row))
            ret += '\n'
        return ret

    def __str__(self):
        return self.__repr__()

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def position_exists(pos):
        if pos.x < 0 or pos.x > (BOARD_HEIGHT - 1):
            return False
        if pos.y < 0 or pos.y > (BOARD_HEIGHT - 1):
            return False
        if pos.y > pos.x:
            return False
        return True

    def positions_around(self):
        x = self.x
        y = self.y
        ret = []
        if DEBUG: print(f"Positions around for {self}")
        surr_positions = [
            Position(x    , y - 1),
            Position(x + 1, y    ),
            Position(x + 1, y + 1),
            Position(x    , y + 1),
            Position(x - 1, y    ),
            Position(x - 1, y - 1),
        ]
        for surr_pos in surr_positions:
            if self.position_exists(surr_pos):
                ret.append(surr_pos)
        return ret

    def jump_position(self, pos):
        jump_x = 2 * (pos.x - self.x) + self.x
        jump_y = 2 * (pos.y - self.y) + self.y
        jump_pos = Position(jump_x, jump_y)
        if not pos in self.positions_around():
            return None
        if self.position_exists(jump_pos):
            return jump_pos
        return None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        if type(other) == type(self):
            if other.x == self.x and other.y == self.y:
                return True
        return False

    
class Move:
    def __init__(self, pos_from, pos_over, pos_to):
        self.pos_from = pos_from
        self.pos_to = pos_to
        self.pos_over = pos_over
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Move {self.pos_from} to {self.pos_to}"


if __name__ == "__main__":
    board = Board()

    # A list of sequential moves to describe the steps taken to get to the
    # current position
    current_moves = []
    # A queue of sets of moves
    moves_list_queue = []
    # List of finishing move sets
    complete_movesets = []

    count = 0
    complete_moves_count = 0
    try:
        while True: # board.piece_count() > 1:
            # Is this a finished moveset
            if board.piece_count() == 1:
                complete_movesets.append(current_moves[:])
                complete_moves_count += 1

            # Is the queue empty
            if len(moves_list_queue) == 0:
                # If there are no moves left then the game is finished
                moves = board.possible_moves()
                if len(moves) == 0:
                    break
                else:
                    moves_list_queue.append(moves)

            # Is the current set of moves empty
            if len(moves_list_queue[-1]) == 0:
                # We need to back pedal one move
                moves_list_queue.pop()
                back_move = current_moves.pop()
                board.backup_move(back_move)
            else:
                # Continue with a move from the list
                next_move = moves_list_queue[-1].pop()
                board.apply_move(next_move)
                current_moves.append(next_move)
                # Add the next lot of moves to the queue
                next_moves = board.possible_moves()
                moves_list_queue.append(next_moves)

            sys.stdout.write('\r' + "count: " + str(count) + " complete moves count: " + str(complete_moves_count) + " length: " + str(len(current_moves)))
            sys.stdout.flush()
            count += 1

    except IndexError as e:
        # I don't want to check if the list is empty every iteration
        # So ill catch the pop error here
        print('\n' + e)
        pass

    # Print all the movesets
    for i in complete_movesets:
        print(i)
    print("Number of complete movesets", len(complete_movesets))

    
    def show_move_steps(moves):
        """ Print the steps to completing the given moves """
        print("With moveset", moves)
        board = Board()
        print(board)
        for i, move in enumerate(moves):
            print(f"Move {i}: {move}")
            board.apply_move(move)
            print(board)

    show_move_steps(complete_movesets[0])
    exit(0)
