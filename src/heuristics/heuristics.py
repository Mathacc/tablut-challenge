from typing import List, Optional

class Heuristics:
    NUM_BLACK=16
    NUM_WHITE=8
    NUM_ESCAPES=16
    NUM_CITADELS=16
    def __init__(self, state):
        self.state = state

    def evaluate_state(self) -> float:
        return 0.0

    def king_position(self, state) -> List[int]:
        king_pos = [-1, -1]
        board = state.get_board()
        for i, row in enumerate(board):
            for j, pawn in enumerate(row):
                if state.get_pawn(i, j).equals_pawn("K"):
                    king_pos = [i, j]
                    break
        return king_pos

    def check_king_position(self, state) -> bool:
        return state.get_pawn(4, 4).equals_pawn("K")

    def check_near_pawns(self, state, position: List[int], target: str) -> int:
        board = state.get_board()
        count = 0
        if board[position[0] - 1][position[1]].equals_pawn(target):
            count += 1
        if board[position[0] + 1][position[1]].equals_pawn(target):
            count += 1
        if board[position[0]][position[1] - 1].equals_pawn(target):
            count += 1
        if board[position[0]][position[1] + 1].equals_pawn(target):
            count += 1
        return count

    def position_near_pawns(self, state, position: List[int], target: str) -> List[List[int]]:
        occupied_positions = []
        board = state.get_board()
        
        if board[position[0] - 1][position[1]].equals_pawn(target):
            occupied_positions.append([position[0] - 1, position[1]])
        if board[position[0] + 1][position[1]].equals_pawn(target):
            occupied_positions.append([position[0] + 1, position[1]])
        if board[position[0]][position[1] - 1].equals_pawn(target):
            occupied_positions.append([position[0], position[1] - 1])
        if board[position[0]][position[1] + 1].equals_pawn(target):
            occupied_positions.append([position[0], position[1] + 1])

        return occupied_positions

    def check_near_king(self, state, position: List[int]) -> bool:
        return self.check_near_pawns(state, position, "K") > 0

    def get_number_of_blocked_escape(self) -> int:
        count = 0
        blocked_escapes = [[1, 1], [1, 2], [1, 6], [1, 7], [2, 1], [2, 7],
                           [6, 1], [6, 7], [7, 1], [7, 2], [7, 6], [7, 7]]
        for pos in blocked_escapes:
            if self.state.get_pawn(pos[0], pos[1]).equals_pawn("BLACK"):
                count += 1
        return count

    def has_white_won(self) -> bool:
        king_pos = self.king_position(self.state)
        return king_pos[0] in [0, 8] or king_pos[1] in [0, 8]

    def safe_position_king(self, state, king_position: List[int]) -> bool:
        return 2 < king_position[0] < 6 and 2 < king_position[1] < 6

    def king_goes_for_win(self, state) -> bool:
        king_pos = self.king_position(state)
        col = row = 0
        if not self.safe_position_king(state, king_pos):
            if king_pos[1] <= 2 or king_pos[1] >= 6:
                col = self.count_free_column(state, king_pos)
            if king_pos[0] <= 2 or king_pos[0] >= 6:
                row = self.count_free_row(state, king_pos)
        return (col + row) > 0

    def count_win_ways(self, state) -> int:
        king_pos = self.king_position(state)
        col = row = 0
        if not self.safe_position_king(state, king_pos):
            if king_pos[1] <= 2 or king_pos[1] >= 6:
                col = self.count_free_column(state, king_pos)
            if king_pos[0] <= 2 or king_pos[0] >= 6:
                row = self.count_free_row(state, king_pos)
        return col + row

    def count_free_row(self, state, position: List[int]) -> int:
        row = position[0]
        column = position[1]
        free_ways = count_right = count_left = 0

        for i in range(column + 1, 9):
            if self.check_occupied_position(state, [row, i]):
                count_right += 1
        if count_right == 0:
            free_ways += 1

        for i in range(column - 1, -1, -1):
            if self.check_occupied_position(state, [row, i]):
                count_left += 1
        if count_left == 0:
            free_ways += 1

        return free_ways

    def count_free_column(self, state, position: List[int]) -> int:
        row = position[0]
        column = position[1]
        free_ways = count_up = count_down = 0

        for i in range(row + 1, 9):
            if self.check_occupied_position(state, [i, column]):
                count_down += 1
        if count_down == 0:
            free_ways += 1

        for i in range(row - 1, -1, -1):
            if self.check_occupied_position(state, [i, column]):
                count_up += 1
        if count_up == 0:
            free_ways += 1

        return free_ways

    def check_occupied_position(self, state, position: List[int]) -> bool:
        return not state.get_pawn(position[0], position[1]).equals("EMPTY")

    def get_num_eaten_positions(self, state) -> int:
        king_pos = self.king_position(state)
        if king_pos == [4, 4]:
            return 4
        elif king_pos in [[3, 4], [4, 3], [5, 4], [4, 5]]:
            return 3
        else:
            return 2
