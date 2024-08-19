from matplotlib import pyplot as plt

def plot(rounds, mean_rounds) -> None:
    # displays graph of scores in separate window
    plt.figure(2)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Rounds')
    plt.plot(rounds)
    plt.plot(mean_rounds)
    plt.ylim(ymin=0)
    #plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_rounds)-1, mean_rounds[-1], str(mean_rounds[-1]))
    plt.show(block=False)
