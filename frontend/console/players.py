from game.exceptions import InvalidMove
from game.models import GameState, Move
from game.player import Player

class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                index = int(input(f"{self.character}'s move: "))
            except ValueError:
                print("Please enter an integer.")
            else:
                try:
                    return game_state.possible_moves[index]
                except InvalidMove:
                    print("Not a valid move.")
        return None
