from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models import GameState, Network, Character # handles circular imports

from game.exceptions import InvalidNetwork, InvalidGameState
    
def validate_network(network : "Network"):
    adj = network.adj
    ra = network.ra
    n = len(adj)
    for i in range(len(adj)):
        for j in range(len(adj)):
            if len(adj[j]) != n:
                raise InvalidNetwork("Adjacency matrix has incorrect shape.")
            if not (0 <= adj[i][j] < ra.num_atoms):
                raise InvalidNetwork("Edges must be labelled by atoms.")
            elif adj[i][j] < ra.num_units and i != j:
                raise InvalidNetwork("Self loop can only be labelled by units.")

def validate_game_state(game_state : "GameState"):
    if len(game_state.network.adj) == 0 and game_state.current_player.value == 'H':
        if not isinstance(game_state.need, int):
            raise InvalidGameState("Heloise must only have to place an atom in round 1.")
        