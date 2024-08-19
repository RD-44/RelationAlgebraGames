import pickle
from pebblegame.dqn.agents import AbelardeAgent, HeloiseAgent
from pebblegame.dqn.aiengine import PebbleGameAI
from pebblegame.dqn.plot_stats import plot
from ras.relalg import RA
import ras
import sys
sys.modules['relalg'] = ras.relalg


def train_both(ra : RA, n : int, name_abelarde : str, name_heloise : str):
    rounds = []
    mean_rounds = []
    total_score = 0
    record = 0
    abelarde_agent = AbelardeAgent(ra, n, name_abelarde)
    heloise_agent = HeloiseAgent(ra, n, name_heloise)
    game = PebbleGameAI(ra, n)
    
    while True:
        if game.num_games % 10 == 0: 
            abelarde_agent.model.save()
            heloise_agent.model.save()

        # get old state 
        state_old_abelarde = abelarde_agent.get_state(game)
        # get move based on current state
        action_abelarde = abelarde_agent.get_action(state_old_abelarde)
        # do the move and get new state
        reward_abelarde, done_abelarde = game.play_abelarde_step(action_abelarde)
        state_new_abelarde = abelarde_agent.get_state(game)

        #TODO: DO NOT train or remember once both players have moved!!
        # if abelarde plays wrong, punish and restart. else, let heloise move. 
        # if heloise plays wrong, punish her and reward abelarde. else, reward her and punish abelarde
        # must implement the play heloise step in pebblegameai

        if done_abelarde:
            # experienced replay - train again on previous moves to improve 
            abelarde_agent.remember(state_old_abelarde, action_abelarde, reward_abelarde, state_new_abelarde, done_abelarde)
            abelarde_agent.train_long_memory()
            record = max(record, game.rounds)
            print('Game', game.num_games, 'Rounds', game.rounds, 'Record', record, ' Abelarde')
            rounds.append(game.rounds)
            total_score += game.rounds
            mean_rounds.append(total_score/game.num_games)
            game.reset()
            plot(rounds, mean_rounds)
            continue
            
        state_old_heloise = state_new_abelarde
        action_heloise = heloise_agent.get_action(state_old_heloise)
        reward_heloise, done_heloise = game.play_heloise_step(action_heloise)
        state_new_heloise = heloise_agent.get_state(game)

        if done_heloise:
            # reward abelard for beating heloise
            abelarde_agent.remember(state_old_abelarde, action_abelarde, 5, state_new_abelarde, done_abelarde)
            abelarde_agent.train_short_memory(state_old_abelarde, action_abelarde, 5, state_new_abelarde, done_abelarde)
            abelarde_agent.train_long_memory()

            # punish heloise for losing
            heloise_agent.remember(state_old_heloise, action_heloise, reward_heloise, state_new_heloise, done_heloise)
            heloise_agent.train_short_memory(state_old_heloise, action_heloise, reward_heloise, state_new_heloise, done_heloise)
            heloise_agent.train_long_memory()

            record = max(record, game.rounds)
            print('Game', game.num_games, 'Score', game.rounds, 'Record', record, ' Heloise')
            rounds.append(game.rounds)
            total_score += game.rounds
            mean_rounds.append(total_score/game.num_games)
            game.reset()
            plot(rounds, mean_rounds)
            continue

        reward_abelarde = -2
        abelarde_agent.train_short_memory(state_old_abelarde, action_abelarde, reward_abelarde, state_new_abelarde, done_abelarde)
        abelarde_agent.remember(state_old_abelarde, action_abelarde, reward_abelarde, state_new_abelarde, done_abelarde)
        heloise_agent.train_short_memory(state_old_heloise, action_heloise, reward_heloise, state_new_heloise, done_heloise)
        heloise_agent.remember(state_old_heloise, action_heloise, reward_heloise, state_new_heloise, done_heloise)

def train_abelarde(ra : RA, n : int, name):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    abelarde_agent = AbelardeAgent(ra, n, name)
    game = PebbleGameAI(ra, n)

    while True:
        # get old state 
        state_old = abelarde_agent.get_state(game)
        # get move based on current state
        action = abelarde_agent.get_action(state_old)
        # do the move and get new state
        reward, done = game.play_abelarde_single(action)
        state_new = abelarde_agent.get_state(game)
        abelarde_agent.train_short_memory(state_old, action, reward, state_new, done)
        abelarde_agent.remember(state_old, action, reward, state_new, done)

        if done:
            # experienced replay - train again on ALL previous moves to improve 
            abelarde_agent.train_long_memory()

            record = max(record, game.rounds)

            print('Game', game.num_games, 'Score', game.rounds, 'Record', record)

            plot_scores.append(game.rounds)
            total_score += game.rounds
            plot_mean_scores.append(total_score/game.num_games)

            if game.num_games % 10 == 0:
                abelarde_agent.save()

            game.reset()
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    with open("library/tests/test_ras/ra4.pickle", "rb") as f:
        ra = pickle.load(f)
    train_abelarde(ra, 5, 'mckenzie_5A')