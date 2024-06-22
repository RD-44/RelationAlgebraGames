from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models import AbelardeState, HeloiseState, Network # handles circular imports

from game.exceptions import InvalidNetwork, InvalidGameState
    
def validate_network(network : "Network") -> None:
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

def validate_heloise_state(game_state : "HeloiseState") -> None:
    if len(game_state.network.adj) == 0:
        if not isinstance(game_state.need, int):
            raise InvalidGameState("Heloise must only have to place an atom in round 1.")
    else:
        if not isinstance(game_state.need, tuple):
            raise InvalidGameState("Heloise does not have a tuple of values.ß")
        elif len(game_state.need) != 4:
            raise InvalidGameState("Tuple must be 4 values.")
        