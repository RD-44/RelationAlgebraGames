from game.models import AbelardeState, HeloiseState
from game.renderers import Renderer

class ConsoleRenderer(Renderer):
    def renderAbelarde(self, game_state: AbelardeState) -> None:
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
        else:
            print("Abalarde moves:")
            if game_state.network.adj:  
                game_state.network.display()
                for i in range(len(game_state.possible_moves)):
                    print(f'Move {i}: ')
                    move = game_state.possible_moves[i].after_state.need
                    edge_label = game_state.network.ra.tochar[game_state.network.adj[move[0]][move[1]]]
                    a, b = game_state.network.ra.tochar[move[2]], game_state.network.ra.tochar[move[3]]
                    print(f"Nodes {move[0]} and {move[1]}, {a};{b} >= {edge_label}\n")
            else:
                print(f"Atoms : {game_state.possible_moves}")
            
    def renderHeloise(self, game_state: HeloiseState) -> None:
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
        else:
            print("Heloise moves: \n")
            for i in range(len(game_state.possible_moves)):
                print(f'Move {i}: ')
                move = game_state.possible_moves[i]
                row = move.after_state.network.adj[-1]
                n = len(row)
                for i in range(n):
                    print(f"Edge {i}->{n-1}: {game_state.network.ra.tochar[row[i]]}")
                print('\n')


def clear_screen() -> None:
    print('\033c')