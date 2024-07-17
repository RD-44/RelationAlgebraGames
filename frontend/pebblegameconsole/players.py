from pebblegame.models import AbelardeState, Character, GameState, HeloiseState, Move
from pebblegame.player import Player

class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        # while not game_state.game_over:
        #     try:
        #         index = int(input(f"{self.character.value}'s move: "))
        #     except ValueError:
        #         print("Please enter an index corresponding to the move.")
        #     else:
        #         try:
        #             return game_state.possible_moves[index]
        #         except IndexError:
        #             print("Not a valid move.")
        # return None
        n = len(game_state.network.adj)
        if game_state.current_player is Character.ABELARDE:
            print(f"Nodes go from 0 to {n-1}")
            x = int(input("Enter node x: "))
            y = int(input("Enter node y: "))
            z = int(input("Enter node z (must not be same as x or y): "))
            print("Atoms:", game_state.network.ra.tochar)
            a = int(input("Enter atom a: "))
            b = int(input("Enter atom b: "))
            incoming = [-1 for _ in range(n)]
            incoming[x] = a
            incoming[y] = game_state.network.ra.converse[b]
            return Move(
                    character=Character.ABELARDE,
                    before_state=game_state,
                    after_state=HeloiseState(game_state.network.add(z, incoming), x, y, z)
                )
        else:
            col = []
            print("Atoms:", game_state.network.ra.tochar)
            for i in range(n):
                if i == game_state.z:
                    if game_state.network.ra.num_units > 1:
                        print(f"Units go from 0 to {game_state.network.ra.num_units}")
                        col.append(int(input(f"Unit labelling edge {i}->{game_state.z}: ")))
                    else:
                        col.append(0)
                else:
                    col.append(int(input(f"Atom labelling edge {i}->{game_state.z}: ")))
            a, b = game_state.network.adj[game_state.x][game_state.z], game_state.network.adj[game_state.z][game_state.y]
            next_network = game_state.network.add(game_state.z, col)
            return Move(
                    character=Character.HELOISE,
                    before_state=game_state,
                    after_state=AbelardeState(next_network, a == next_network.adj[game_state.x][game_state.z] and b == next_network.adj[game_state.z][game_state.y])
                )




