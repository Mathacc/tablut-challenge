from heuristics import Heuristics
from state import State  # Assuming the existence of a State class similar to Java's structure

class WhiteHeuristics(Heuristics):
    """
    WhiteHeuristics is a subclass of Heuristics for evaluating the board state 
    from the perspective of the white player in the game Ashton Tablut.
    """
    THRESHOLD_BEST = 2
    BEST_POSITIONS = [(2, 3), (3, 5), (5, 3), (6, 5)]
    NUM_BEST_POSITION = len(BEST_POSITIONS)
    
    def __init__(self, state: State):
        """
        Initializes the WhiteHeuristics class with the given state.
        Args:
            state (State): The current state of the game.
        Attributes:
            weights (dict): A dictionary containing the weights for different heuristic factors.
                - "bestPositions": Weight for the best positions heuristic.
                - "numberOfBlackEaten": Weight for the number of black pieces eaten heuristic.
                - "numberOfWhiteAlive": Weight for the number of white pieces alive heuristic.
                - "numberOfWinEscapesKing": Weight for the number of winning escapes for the king heuristic.
                - "blackSurroundKing": Weight for the black pieces surrounding the king heuristic.
                - "protectionKing": Weight for the protection of the king heuristic.
            keys (list): A list of keys from the weights dictionary.
            flag (bool): A flag to enable or disable debug printing.
        """
        
        super().__init__(state)
        self.weights = {
            "bestPositions": 2.0,
            "numberOfBlackEaten": 20.0,
            "numberOfWhiteAlive": 35.0,
            "numberOfWinEscapesKing": 18.0,
            "blackSurroundKing": 7.0,
            "protectionKing": 18.0
        }
        self.keys = list(self.weights.keys())
        self.flag = False  # Flag to enable/disable debug printing
    
    def evaluate_state(self) -> float:
        """
        Evaluate the current state of the game and return a utility value.
        This method calculates a utility value based on several heuristic factors
        that represent the current state of the game. The factors include:
        - Best positions occupied by white pawns.
        - Number of white pawns alive.
        - Number of black pawns eaten.
        - Black pawns surrounding the king.
        - Protection of the king.
        - Number of winning escape routes for the king.
        The utility value is computed as a weighted sum of these factors.
        Returns:
            float: The utility value representing the current state of the game.
        """
        utility_value = 0.0
        values = {
            "bestPositions": self.get_number_on_best_positions() / self.NUM_BEST_POSITION,
            "numberOfWhiteAlive": self.state.get_number_of(State.Pawn.WHITE) / self.NUM_WHITE,
            "numberOfBlackEaten": (self.NUM_BLACK - self.state.get_number_of(State.Pawn.BLACK)) / self.NUM_BLACK,
            "blackSurroundKing": (self.get_num_eaten_positions() - self.check_near_pawns(self.king_position(), State.Pawn.BLACK)) / self.get_num_eaten_positions(),
            "protectionKing": self.protection_king(),
            "numberOfWinEscapesKing": self.count_win_ways() / 4 if self.count_win_ways() > 1 else 0.0
        }

        for key in self.keys:
            utility_value += self.weights[key] * values[key]
            if self.flag:
                print(f"{key}: {self.weights[key]} * {values[key]} = {self.weights[key] * values[key]}")
        
        return utility_value
    
    def get_number_on_best_positions(self) -> int:
        """
        Calculate the number of white pawns positioned in the best positions.

        This method counts the number of white pawns that are located in the 
        predefined best positions on the board. It only performs this calculation 
        if the current number of white pawns is greater than or equal to the 
        difference between the total number of white pawns and a specified threshold.

        Returns:
            int: The number of white pawns in the best positions.
        """
        num = 0
        if self.state.get_number_of(State.Pawn.WHITE) >= self.NUM_WHITE - self.THRESHOLD_BEST:
            for pos in self.BEST_POSITIONS:
                if self.state.get_pawn(*pos) == State.Pawn.WHITE:
                    num += 1
        return num
    
    def protection_king(self) -> float:
        """
        Evaluates the protection level of the king in the game.
        This heuristic function calculates a score based on the proximity and 
        positioning of white pawns around the king. The score is influenced by 
        the number of black pawns near the king, the number of positions where 
        pawns have been eaten, and the strategic positioning of white pawns.
        Returns:
            float: A score representing the protection level of the king. 
               The score ranges from 0.0 (no protection) to 1.0 (maximum protection).
        """
        VAL_NEAR = 0.6
        VAL_TOT = 1.0
        result = 0.0
        king_pos = self.king_position()
        pawns_positions = self.position_near_pawns(king_pos, State.Pawn.BLACK)

        if len(pawns_positions) == 1 and self.get_num_eaten_positions() == 2:
            enemy_pos = pawns_positions[0]
            target_pos = self.calculate_target_position(king_pos, enemy_pos)
            
            if self.state.get_pawn(*target_pos) == State.Pawn.WHITE:
                result += VAL_NEAR

            if target_pos[0] in {0, 8} or target_pos[1] in {0, 8}:
                result = 1.0 if self.state.get_pawn(*target_pos) == State.Pawn.EMPTY else 0.0
            else:
                contribution_per_n = (VAL_TOT - VAL_NEAR) / (2 if self.is_near_citadel_or_throne(target_pos) else 3)
                result += contribution_per_n * self.check_near_pawns(target_pos, State.Pawn.WHITE)
                
        return result
    
    def calculate_target_position(self, king_pos, enemy_pos):
        """
        Calculate the target position for the king based on the enemy's position.

        This method determines the next position the king should move to in order to avoid the enemy.
        If the enemy is in the same row as the king, the king will move vertically.
        If the enemy is in the same column as the king, the king will move horizontally.

        Args:
            king_pos (tuple): A tuple (x, y) representing the current position of the king.
            enemy_pos (tuple): A tuple (x, y) representing the current position of the enemy.

        Returns:
            tuple: A tuple (x, y) representing the target position for the king.
        """
        if enemy_pos[0] == king_pos[0]:
            return (king_pos[0], king_pos[1] + 1) if enemy_pos[1] < king_pos[1] else (king_pos[0], king_pos[1] - 1)
        else:
            return (king_pos[0] + 1, king_pos[1]) if enemy_pos[0] < king_pos[0] else (king_pos[0] - 1, king_pos[1])
    
    def is_near_citadel_or_throne(self, pos):
        return pos in [(4, 2), (4, 6), (2, 4), (6, 4), (3, 4), (5, 4), (4, 3), (4, 5)]
