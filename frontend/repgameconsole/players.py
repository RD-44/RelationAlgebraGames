from repgame.models import GameState, Move
from repgame.player import Player

class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                index = int(input(f"{self.character.value}'s move: "))
            except ValueError:
                print("Please enter an index corresponding to the move.")
            else:
                try:
                    return game_state.possible_moves[index]
                except IndexError:
                    print("Not a valid move.")
        return None
