from typing import TYPE_CHECKING

if TYPE_CHECKING: # handles circular imports
    from pebblegame.models import HeloiseState, Network
    from pebblegame.engine import PebbleGame

from pebblegame.exceptions import InvalidGameState


def validate_game(game : "PebbleGame"):
    from pebblegame.models import Character
    if game.player1.character is not Character.ABELARDE:
        raise InvalidGameState("Player 1 must be Abelarde.")
    if game.player2.character is not Character.HELOISE:
        raise InvalidGameState("Player 2 must be Heloise.")