from game.exceptions import UnknownGameScore
from game.models import Character, GameState, Move
import math

def find_best_move(game_state : GameState) -> Move | None:
    maximiser = game_state.current_player
    best_move = None
    best_score = -math.inf
    alpha = -math.inf
    beta = math.inf
    for move in game_state.possible_moves:
        score = minimax(move, maximiser, alpha, beta)
        alpha = max(alpha, score)
        if score >= best_score : 
            best_move = move
            best_score = score
    return best_move


def minimax(move: Move, maximiser: Character, alpha : int, beta : int, maximise: bool = False) -> int:
    if move.after_state.game_over: return evaluate_score(move.after_state, maximiser)
    if maximise:
        best_score = -math.inf
        for next_move in move.after_state.possible_moves:
            score = minimax(next_move, maximiser, alpha, beta, not maximise)
            best_score = max(best_score, score)
            if score >= beta : break
            alpha = max(alpha, score)   
        return best_score
    else:
        best_score = math.inf
        for next_move in move.after_state.possible_moves:
            score = minimax(next_move, maximiser, alpha, beta, not maximise)
            best_score = min(score, best_score)
            if score <= alpha : break
            beta = min(beta, score)
        return best_score
    
def evaluate_score(game_state: GameState, maximiser: Character):
    if not game_state.game_over:
        raise UnknownGameScore("Cannot get game score when game is not over.")
    if game_state.winner is maximiser:
        return math.inf
    else:
        return -math.inf

