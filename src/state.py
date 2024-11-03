from enum import Enum
from typing import List, Optional
from copy import deepcopy

class Turn(Enum):
    """
    Enum representing the possible game turns and end states.
    - WHITE: White player's turn
    - BLACK: Black player's turn
    - WHITEWIN: White player wins
    - BLACKWIN: Black player wins
    - DRAW: Game ends in a draw
    """
    WHITE = "W"
    BLACK = "B"
    WHITEWIN = "WW"
    BLACKWIN = "BW"
    DRAW = "D"

    def equals_turn(self, other: str) -> bool:
        """
        Checks if this Turn equals the given string.

        :param other: The string to compare with this Turn
        :return: True if equal, False otherwise
        """
        return self.value == other

class Pawn(Enum):
    """
    Enum representing the types of pieces (pawns) that can occupy board cells.
    - EMPTY: An empty cell
    - WHITE: A cell occupied by a white pawn
    - BLACK: A cell occupied by a black pawn
    - THRONE: The throne position on the board
    - KING: The king piece
    """
    EMPTY = "O"
    WHITE = "W"
    BLACK = "B"
    THRONE = "T"
    KING = "K"

    def equals_pawn(self, other: str) -> bool:
        """
        Checks if this Pawn equals the given string.

        :param other: The string to compare with this Pawn
        :return: True if equal, False otherwise
        """
        return self.value == other

class State:
    """
    Represents the state of a game, including the board configuration and the player's turn.
    The board is a 2D grid of Pawn objects, and the turn indicates which player's move it is.
    """
    
    def __init__(self):
        """
        Initializes an empty game state with no board or turn set.
        """
        self.board: Optional[List[List[Pawn]]] = None
        self.turn: Optional[Turn] = None

    def get_board(self) -> List[List[Pawn]]:
        """
        Returns the current board configuration.

        :return: 2D list of Pawn objects representing the board
        """
        return self.board

    def board_string(self) -> str:
        """
        Creates a string representation of the board, with each row on a new line.

        :return: A formatted string representing the board
        """
        result = []
        for row in self.board:
            result.append("".join(pawn.value for pawn in row))
        return "\n".join(result)

    def __str__(self) -> str:
        """
        Converts the state to a string, showing the board and current turn.

        :return: A string representation of the board and turn
        """
        board_repr = self.board_string()
        return f"{board_repr}\n-\n{self.turn.value if self.turn else ''}"

    def to_linear_string(self) -> str:
        """
        Creates a linear (single-line) string representation of the board and turn.

        :return: A string representing the board and turn without line breaks
        """
        board_repr = self.board_string().replace("\n", "")
        return f"{board_repr}{self.turn.value if self.turn else ''}"

    def get_pawn(self, row: int, column: int) -> Pawn:
        """
        Retrieves the pawn at a specific board position.

        :param row: Row index of the pawn
        :param column: Column index of the pawn
        :return: The Pawn at the specified position
        """
        return self.board[row][column]

    def remove_pawn(self, row: int, column: int):
        """
        Removes a pawn from a specific position on the board by setting it to EMPTY.

        :param row: Row index of the position
        :param column: Column index of the position
        """
        self.board[row][column] = Pawn.EMPTY

    def set_board(self, board: List[List[Pawn]]):
        """
        Sets the board configuration.

        :param board: 2D list of Pawn objects representing the new board
        """
        self.board = board

    def get_turn(self) -> Turn:
        """
        Gets the current player's turn.

        :return: The current Turn
        """
        return self.turn

    def set_turn(self, turn: Turn):
        """
        Sets the current player's turn.

        :param turn: The Turn to set as the current turn
        """
        self.turn = turn

    def __eq__(self, other) -> bool:
        """
        Checks if two states are equal by comparing their boards and turns.

        :param other: The other State to compare with
        :return: True if states are equal, False otherwise
        """
        if not isinstance(other, State):
            return False
        return self.board == other.board and self.turn == other.turn

    def __hash__(self) -> int:
        """
        Generates a hash code for the state based on the board and turn.

        :return: Hash code of the state
        """
        return hash((str(self.board), self.turn))

    def get_box(self, row: int, column: int) -> str:
        """
        Converts a board position to a human-readable string format.

        :param row: Row index of the position
        :param column: Column index of the position
        :return: A string representing the board position (e.g., 'a1')
        """
        col_letter = chr(column + 97)
        return f"{col_letter}{row + 1}"

    def clone(self) -> 'State':
        """
        Creates a deep copy (clone) of the current state.

        :return: A new State object with a copied board and turn
        """
        cloned_state = State()
        cloned_state.set_board(deepcopy(self.board))
        cloned_state.set_turn(self.turn)
        return cloned_state

    def get_number_of(self, color: Pawn) -> int:
        """
        Counts the number of cells containing a specific pawn type.

        :param color: The Pawn type to count (e.g., WHITE, BLACK)
        :return: The number of cells containing the specified pawn type
        """
        return sum(pawn == color for row in self.board for pawn in row)
