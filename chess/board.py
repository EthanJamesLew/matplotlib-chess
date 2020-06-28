""" Model Chess Board
Ethan Lew
elew@pdx.edu
"""
import string
import numpy as np


class ChessBoard:
    """ represents a chess board with pieces on it, where

    - pieces can be added
    - pieces can be removed
    - pieces can be moved
    - valid next moves can be determined
    """
    @staticmethod
    def idx_to_pos(pos):
        """convert index of chess board to chess position"""
        if type(pos) is str:
            return pos
        assert len(pos) == 2
        assert pos[0] < 26
        return string.ascii_lowercase[pos[0]] + f'{pos[1]}'

    @staticmethod
    def pos_to_idx(s):
        if type(s) is tuple:
            return s
        assert s[0] in string.ascii_lowercase
        try:
            return (string.ascii_letters.index(s[0]), int(s[1:])-1)
        except ValueError as exc:
            raise ValueError(f"chess position {s} cannot be interpret {s[1:]} as an integer")

    def __init__(self):
        self._size = 8
        self._positions = {}
        self._rules = {}
        self._need_update = False
        self._uncapturable = []

    def add_piece(self, pos, color, rules):
        """add a chess piece to the board
        :param pos: position on board
        :param color: white or black
        :param rules: rules describing piece
        :return: None
        """
        pos = self.pos_to_idx(pos)
        name = rules["piece_name"]
        if name not in self._rules:
                self._rules[name] = rules
                if rules['capturable'] is False:
                    self._uncapturable += [name]
        self._positions[tuple(pos)] = (name, color)
        self._need_update = True
        self._available_positions = {}

    def remove_piece(self, pos):
        """given a valid piece at position pos, remove it from the check board"""
        pos = self.pos_to_idx(pos)
        assert self.is_piece(pos), f"ChessBoard asked to remove piece at pos {pos} where no piece exists"
        del self._positions[pos]
        self._need_update = True

    def move_piece(self, pos, pos_new):
        """ given a piece at a position, change to position new
        :param pos: board index
        :param pos_new: new board index
        :return: None
        """
        pos = self.pos_to_idx(pos)
        pos_new = self.pos_to_idx(pos_new)
        assert tuple(pos) in self._positions
        self._positions[tuple(pos_new)] = self._positions.pop(tuple(pos))
        self._need_update = True

    def get_moves_positional(self, pos):
        def is_clear(cols, rows):
            is_c = True
            for r in rows:
                for c in cols:
                    is_c = is_c and (not self.is_piece((c, r)))
            return is_c

        pos = self.pos_to_idx(pos)
        if not self.is_piece(pos):
            return []
        else:
            # load object
            name, color = self._positions[tuple(pos)]
            moves = []
            if color is True:
                # pawn twice advance condition
                if (name.lower() == 'pawn'):
                    if (pos[1] == 1) and is_clear([pos[0]], [pos[1]+1, pos[1]+2]):
                        return [(pos[0], pos[1]+2)]
                elif (name.lower() == 'king') and pos == (4, 0):
                    if self.is_piece((0, 0)):
                        name_r, color = self._positions[(0, 0)]
                        if is_clear([1, 2, 3], [0]) and name_r.lower() == 'rook' and color:
                            moves += [(2, 0)]
                    if self.is_piece((7, 0)):
                        name_r, color = self._positions[(7, 0)]
                        if is_clear([5, 6], [0]) and name_r.lower() == 'rook' and color:
                            moves += [(6, 0)]
                    return moves
            else:
                # pawn twice advance condition
                if (name.lower() == 'pawn'):
                    if (pos[1] == 6) and is_clear([pos[0]], [pos[1]-1, pos[1]-2]):
                        return [(pos[0], pos[1]-2)]
                elif (name.lower() == 'king') and pos == (4, 7):
                    moves = []
                    if self.is_piece((0, 7)):
                        name_r, color = self._positions[(0, 7)]
                        if is_clear([1, 2, 3], [7]) and name_r.lower() == 'rook' and not color:
                            moves += [(2, 7)]
                    if self.is_piece((7, 7)):
                        name_r, color = self._positions[(7, 7)]
                        if is_clear([5, 6], [7]) and name_r.lower() == 'rook' and not color:
                            moves += [(6, 7)]
                    return moves
            return []


    def get_moves(self, pos):
        """ given a position, determine possible moves from a piece there (returns nothing if no piece is present)
        :param pos: chess position
        :return: list of moves
        """
        pos = self.pos_to_idx(pos)
        if not self._need_update:
            if pos in self._available_positions:
                return self._available_positions[pos]
            else:
                return []
        if not self.is_piece(pos):
            return []
        else:
            # load object
            name, color = self._positions[tuple(pos)]
            rules = self._rules[name]

            # direction multipliers
            direction_multiplier = np.array([1, 1]) if color is True else np.array([1, -1])
            x_mults = [1] + ([-1] if rules["x_symmetry"] is True else [])
            y_mults = [1] + ([-1] if rules["y_symmetry"] is True else [])
            advance_group = np.array(rules["advance_group"])

            # determine capture group criteria
            c_temp = rules["capture_group"]
            has_capture = c_temp is not False
            if has_capture:
                capture_group = np.array(c_temp)

            # store moves in here
            moves = []

            # determine maximum extensions to piece
            if rules["extensible"]:
                upper_bound = int(np.ceil(np.sqrt(self._size**2)))
            else:
                upper_bound = 1

            for xm in x_mults:
                for ym in y_mults:
                    # iterate through advance group
                    for g in advance_group:
                        for ie in range(1, upper_bound+1):
                            pos_advance = tuple(self.constrain(tuple(np.array(pos)+ie * direction_multiplier * np.array([xm, 1]) * np.array([1, ym]) * np.array(g))))
                            if self.is_piece_color(pos_advance, color):
                                break
                            if pos_advance:
                                moves += [pos_advance]
                            if not pos_advance:
                                # extends past board, leave
                                break
                            if self.is_piece(pos_advance) and rules["blockable"]:
                                # is blocked, leave
                                break

                    # iterate through capture group
                    if has_capture:
                        for c in capture_group:
                            for ic in range(1, upper_bound+1):
                                pos_capture = tuple(self.constrain(tuple(np.array(pos)+ic * direction_multiplier * np.array([xm, 1]) * np.array([1, ym]) * np.array(c))))
                                if self.is_piece_color(pos_capture, color):
                                    break
                                if pos_capture and self.is_piece(pos_capture):
                                    moves += [pos_capture]
                                if not pos_capture:
                                    # extends past board, leave
                                    break
                                if self.is_piece(pos_capture) and rules["blockable"]:
                                    # is blocked, leave
                                    break
            return moves + self.get_moves_positional(pos)

    def update(self):
        if self._need_update:
            self._available_positions = {p: self.get_moves(p) for p in self._positions}
            self._need_update = False

    def constrain(self, move):
        """if move exists in chessboard, return it, else return nothing"""
        move = self.pos_to_idx(move)
        def limit(s):
            return s < self._size and s >= 0
        is_valid = limit(move[0]) and limit(move[1])
        return move if is_valid else []

    def is_piece(self, pos):
        """determine whether piece exists at a given position"""
        pos = self.pos_to_idx(pos)
        if tuple(pos) in self._positions:
            return True
        else:
            return False

    def is_piece_color(self, pos, color):
        pos = self.pos_to_idx(pos)
        if self.is_piece(pos):
            name, pos_color = self._positions[pos]
            if color is pos_color:
                return True
            else:
                return False
        else:
            return False

    @property
    def positions(self):
        return [k for k, i in self._positions.items()]

    @property
    def board_size(self):
        return self._size
