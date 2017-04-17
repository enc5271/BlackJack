from BlackJack import *
import numpy as np
import matplotlib.pyplot as plt

#Initialize deaerl's policy.
#The dealer's policy is fixed to hit on 16 or less, and stay for >= 17.
dealerPolicy = np.zeros(22)
for i in range(17,22):
    # action[1] = stay. action[0] = hit.
    dealerPolicy[i] = 1

#Agent only stays on 20 and 21.
agentPolicy = np.zeros(22)
#XXX Make sure this is for policy 20 and 21
agentPolicy[20] = 1
agentPolicy[21] = 1
#Initialize value function with all zeros.
valueFunction = np.zeros(22)

returns = np.zeros((22,2))
if __name__ == "__main__":
    game = BlackJack(agentPolicy, dealerPolicy)
    for i in range(10,000):
        states,R = game.playEpisode()
        for state in states:
            returns[state][0] += state
            returns[state][1] += 1
            valueFunction[state] = returns[state][0]/returns[state][1]

    plt.plot(range(22),valueFunction)
    plt.show()
