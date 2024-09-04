import repgame
from repgame.exceptions import UnknownGameScore
from repgame.models import Character, GameState, Move
import math

def find_best_move(game_state : GameState) -> Move | None:
    maximiser = game_state.current_player
    best_move = None
    best_score = -math.inf
    alpha = -math.inf
    beta = math.inf
    depth = 3
    for move in game_state.possible_moves:
        score = minimax(move, maximiser, alpha, beta, depth-1)
        alpha = max(alpha, score)
        if score >= best_score : 
            best_move = move
            best_score = score
    return best_move

def minimax(move: Move, maximiser: Character, alpha : int, beta : int, depth : int, maximise: bool = False) -> int:
    if move.after_state.game_over or depth == 0: return evaluate_score(move.after_state, maximiser)
    if maximise:
        best_score = -math.inf
        for next_move in move.after_state.possible_moves:
            score = minimax(next_move, maximiser, alpha, beta, depth-1, not maximise)
            best_score = max(best_score, score)
            if score >= beta : break
            alpha = max(alpha, score)   
        return best_score
    else:
        best_score = math.inf
        for next_move in move.after_state.possible_moves:
            score = minimax(next_move, maximiser, alpha, beta, depth-1, not maximise)
            best_score = min(score, best_score)
            if score <= alpha : break
            beta = min(beta, score)
        return best_score
    # print("Maximiser:", maximiser, "Move:", move, " Score:", score)
        
    
def evaluate_score(game_state: GameState, maximiser: Character):
    if game_state.current_player is maximiser:
        return len(game_state.possible_moves)
    else:
        return -len(game_state.possible_moves)
    
# Heuristics 
def freqs_squared(game_state : GameState, maximiser : Character):
    score = 0
    counts = {}
    adj = game_state.network.adj
    for i in range(len(adj)):
        for j in range(i, len(adj)):
            a = adj[i][j]
            if a in counts:
                counts[a] += 1
            elif (conv := game_state.network.ra.converse[a]) in counts:
                counts[conv] += 1
            else:
                counts[a] = 1
    score = sum(map(lambda x : x**2, counts.values()))
    if maximiser is Character.ABELARDE:
        score = -score
    #print(score)
    return score

def num_moves(game_state : GameState, maximiser : Character):
    n = len(game_state.possible_moves)
    if game_state.current_player is maximiser:
        return n
    return -n

def heloise_moves(game_state : GameState, maximiser : Character):
    # here we assume that the heuristic is calcululated when it is heloise's turn
    if maximiser is Character.HELOISE:
        return len(game_state.possible_moves)
    return -len(game_state.possible_moves)
