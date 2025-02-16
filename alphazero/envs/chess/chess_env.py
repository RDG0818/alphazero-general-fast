from alphazero.Game import GameState
from typing import List, Tuple, Any
import chess

from alphazero.envs.chess.ChessLogic import *
import string

DIGS = string.digits + string.ascii_letters

NUM_PLAYERS = 2
BOARD_SIZE = 8
ACTION_SIZE = 1968 # This is length of uci strings, so this may not be correct
NUM_CHANNELS = 18
OBSERVATION_SIZE = (NUM_CHANNELS, BOARD_SIZE, BOARD_SIZE)


# TODO: Use https://github.com/Unimax/alpha-zero-general-chess-and-battlesnake/blob/master/chesspy/ChessGame.py for
#  implementation
# currently in ChessLogic

def _int2base(x, base, length):
    if x < 0:
        sign = -1
    elif x == 0:
        return [DIGS[0]]*length
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(DIGS[int(x % base)])
        x //= base

    if sign < 0:
        digits.append('-')

    while len(digits) < length: digits.append('0')
    return list(map(lambda x: int(x, base), digits))


class Game(GameState):
    def __init__(self):
        board = Game._get_board()
        self.uci = set(create_uci_labels())
        super().__init__(board)

    @staticmethod
    def _get_board():
        return chess.Board()

    def __eq__(self, other) -> bool:
        return (
            self._board == other._board
            and self._player == other._player
            and self.turns == other.turns
        )

    def clone(self):
        g = ChessGame()
        g._board = self._board.copy()
        g._player = self._player
        g._turns = self.turns
        return g

    @staticmethod
    def action_size() -> int:
        return ACTION_SIZE

    @staticmethod
    def observation_size() -> Tuple[int, int, int]:
        return OBSERVATION_SIZE
    
    @staticmethod
    def has_draw() -> bool:
        return True

    def valid_moves(self): 
        legal_set = {move.uci() for move in self.board.legal_moves}
        mask = np.array([1 if move in legal_set else 0 for move in self.uci], dtype=np.uint8)
        return mask

    @classmethod
    def num_players(self):
        return 2

    def play_action(self, action) -> None:
        # if action not in self.uci:
        #     return # TODO: Better error handling
        # We are assuming that action is a legal move, should be handled in valid_moves
        move = chess.Move.from_uci(action) # Could be faster to do indexing/hashing instead of strings
        
        # if move not in self._board.legal_moves:
        #     return # TODO: Better error handling
        
        self._board.push(move)
        self._update_turn()


    def win_state(self) -> Tuple[bool, int]:
        result = [False, False, False] # For White, Black, and Draw
        if self._board.is_checkmate():
            if self._board.turn == chess.WHITE: result[0] = True
            else: result[1] = True
        elif self._board.is_stalemate(): result[2] = True # TODO: add other draw conditions

        return np.array(result, dtype=np.uint8)

    def observation(self):
        return all_input_planes(self._board.fen())


    def symmetries(self, pi) -> List[Tuple[Any, int]]:
        pass #idk if chess should even have this
    
    def render(self):
        print()
        print(self._board) 
        print()
