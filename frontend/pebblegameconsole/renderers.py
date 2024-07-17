from pebblegame.models import AbelardeState, HeloiseState
from pebblegame.renderers import Renderer

class ConsoleRenderer(Renderer):
    def renderabelarde(self, game_state: AbelardeState) -> None:
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
            game_state.network.display(True)
        else:
            print("Abelarde moves:")
            game_state.network.display()
            for i in range(len(game_state.possible_moves)):
                print(f'Move {i}: ')
                after = game_state.possible_moves[i].after_state
                edge_label = game_state.network.ra.tochar[after.network.adj[after.x][after.y]]
                a, b = after.network.ra.tochar[after.network.adj[after.x][after.z]], after.network.ra.tochar[after.network.adj[after.z][after.y]]
                print(f"x={after.x}, y={after.y}, z={after.z}, {a};{b} >= {edge_label}\n")
            
    def renderheloise(self, game_state: HeloiseState) -> None:
        game_state.network.display()
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
            game_state.network.display(True)
        else:
            print("Heloise moves: \n")
            for i in range(len(game_state.possible_moves)):
                print(f'Move {i}: \n')
                move = game_state.possible_moves[i]
                n = len(game_state.network.adj)
                for i in range(n):
                    print(f"Edge {i}->{game_state.z}: {game_state.network.ra.tochar[move.after_state.network.adj[i][game_state.z]]}")
                print('\n')
