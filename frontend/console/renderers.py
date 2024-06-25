from game.models import AbelardeState, HeloiseState
from game.renderers import Renderer

class ConsoleRenderer(Renderer):
    def renderabelarde(self, game_state: AbelardeState) -> None:
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
            game_state.network.display(True)
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
                choices = [*map(game_state.network.ra.tochar.get, range(game_state.network.ra.num_atoms))]
                print('Atoms:', end=' ')
                print(*choices, sep=', ')
                print("Enter an index corresponding to the atom.")

            
    def renderheloise(self, game_state: HeloiseState) -> None:
        if game_state.winner:
            print(f'{game_state.winner.value} wins.')
            game_state.network.display(True)
        else:
            if not game_state.network.adj:
                print(f"\nAbelarde chose atom {game_state.need}")
            else:
                x, y, a, b = game_state.need
                a, b = game_state.network.ra.tochar[a], game_state.network.ra.tochar[b]
                print(f"\nNode {(z:=len(game_state.network.adj))} has been added to the network. N({x},{z})={a}, N({z},{y})={b}. Heloise must label all new edges.\n")
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