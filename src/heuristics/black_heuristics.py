
from heuristics.heuristics import Heuristics
from state import State

class BlackHeuristics(Heuristics):
    RHOMBUS_POSITIONS = "rhombusPositions"
    WHITE_EATEN = "numberOfWhiteEaten"
    BLACK_ALIVE = "numberOfBlackAlive"
    BLACK_SURROUND_KING = "blackSurroundKing"

    THRESHOLD = 10
    NUM_TILES_ON_RHOMBUS = 8

    def __init__(self, state):
        self.state = state
        self.weights = {
            self.BLACK_ALIVE: 35.0,
            self.WHITE_EATEN: 48.0,
            self.BLACK_SURROUND_KING: 15.0,
            self.RHOMBUS_POSITIONS: 2.0
        }
        self.keys = list(self.weights.keys())

        self.rhombus = [
            (1, 2), (1, 6),
            (2, 1), (2, 7),
            (6, 1), (6, 7),
            (7, 2), (7, 6)
        ]

        self.flag = False
        self.number_of_black = 0
        self.number_of_white_eaten = 0

    def evaluate_state(self):
        utility_value = 0.0

        self.number_of_black = self.state.get_number_of("BLACK") / self.NUM_BLACK
        self.number_of_white_eaten = (self.NUM_WHITE - self.state.get_number_of("WHITE")) / self.NUM_WHITE
        pawns_near_king = self.check_near_pawns(self.state, self.king_position(self.state), "BLACK") / self.get_num_eaten_positions(self.state)
        number_of_pawns_on_rhombus = self.get_number_on_rhombus() / self.NUM_TILES_ON_RHOMBUS

        if self.flag:
            print(f"Number on rhombus: {number_of_pawns_on_rhombus}")
            print(f"Pawns near the king: {pawns_near_king}")
            print(f"White pawns eaten: {self.number_of_white_eaten}")
            print(f"Black pawns: {self.number_of_black}")

        atomic_utilities = {
            self.BLACK_ALIVE: self.number_of_black,
            self.WHITE_EATEN: self.number_of_white_eaten,
            self.BLACK_SURROUND_KING: pawns_near_king,
            self.RHOMBUS_POSITIONS: number_of_pawns_on_rhombus
        }

        for key in self.keys:
            utility_value += self.weights[key] * atomic_utilities[key]
            if self.flag:
                print(f"{key}: {self.weights[key]} * {atomic_utilities[key]} = {self.weights[key] * atomic_utilities[key]}")

        return utility_value

    def get_number_on_rhombus(self):
        if self.state.get_number_of("BLACK") >= self.THRESHOLD:
            return self.get_values_on_rhombus()
        else:
            return 0

    def get_values_on_rhombus(self):
        count = 0
        for x, y in self.rhombus:
            if self.state.get_pawn(x, y) == "BLACK":
                count += 1
        return count
