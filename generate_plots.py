"""
Regenerates every figure used in the README:
  plots/convergence.png    - how much state values still move per 10k games
  plots/value_histogram.png - distribution of learned state values after training
  plots/win_draw_rates.png  - trained agent (O) vs. an agent (X) with varying randomness

Run from the project directory:
    python3 generate_plots.py
"""
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import Board
import Game

random.seed(42)

board = Board.Board()
game = Game.Game(board)
game.learn_N_games(
    500000,
    histogram_path='plots/value_histogram.png',
    convergence_path='plots/convergence.png',
)
game.save_game_state('RL_TIC_TAC.pickle')

epsilons = [0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
wins, draws = [], []
for eps in epsilons:
    _, win2, draw = game.auto_play_N_games(10000, eps, 0)
    wins.append(win2)
    draws.append(draw)

plt.figure()
plt.plot(epsilons, wins, color='blue', linewidth=2, label='Wins')
plt.plot(epsilons, draws, color='red', linewidth=2, label='Draws')
plt.title('Wins/Draws by Randomness of Agent1')
plt.xlabel('Agent1 epsilon')
plt.ylabel('Num Game Results')
plt.legend()
plt.savefig('plots/win_draw_rates.png')

print('Wrote plots/convergence.png, plots/value_histogram.png, plots/win_draw_rates.png')
