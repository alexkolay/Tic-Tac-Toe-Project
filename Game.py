import Board
import random
import pickle

from matplotlib import pyplot as plt

class Game:
    # initializes a Game constructor
    def __init__(self,board):
        self.states = {}
        self.board = board
        self.learning_rate = 0.1
        self.epsilon = 0.3
        self.old_states = {}
        self.convergence_stats=[]
        self.state_stats = {}
        self.win1=0
        self.win2=0
        self.draw = 0

    # updates the state value using the state and next state's old values
    def update_state_value(self, state, next_state):
        state_value = 0
        state_stats = 0
        if state in self.states:
            state_value = self.states[state]
            state_stats = self.state_stats[state]
        next_state_value = 0
        if next_state in self.states:
            next_state_value = self.states[next_state]

        new_state_value = state_value + self.learning_rate * (next_state_value - state_value)
        self.states[state] = new_state_value
        state_stats += 1
        self.state_stats[state] = state_stats

        #print(f'state={state_value}  next_state={next_state_value} new_value={new_state_value}')
    # uses the explore method, which makes a random move for a certain player
    def explore_only(self, moves, player):
        (row,column) = random.choice(moves)
        self.board.make_move(row, column, player)
    # returns the move with the maximum value
    def get_max_move(self,next_states):
        max_value = -100000
        max_move = None
        for (move, value) in next_states:
            if value > max_value:
                max_value = value
                max_move = move
        return max_move
    # returns the move with the minimum value
    def get_min_move(self,next_states):
        min_value = 100000
        min_move = None
        for (move, value) in next_states:
            if value < min_value:
                min_value = value
                min_move = move
        return min_move
    # uses the explore-exploit method for determining which move to make
    def explore_exploit(self,moves, player, epsilon, debug):
        next_states = []
        for move in moves:
            (row,column) = move
            self.board.make_move(row,column,player)
            next_state = self.board.get_state()
            if next_state in self.states:
                next_value = self.states[next_state]
            else:
                next_value = 0

            next_states.append((move,next_value))
            self.board.reset_move(row,column)

        random_value = random.random()
        if random_value < epsilon:
            (row,column) = random.choice(moves)
            self.board.make_move(row, column, player)
        else:
            if player == 'X':
                (row,column) = self.get_max_move(next_states)
            else:
                (row,column) = self.get_min_move(next_states)
            self.board.make_move(row, column, player)
            if debug:
                print(str(next_states))
                print(str((row,column)))
                print('Exploit')
        square = (row, column)
        return square

    # helps generate a move for the first player (only uses explore in learning phase)
    def make_agent1_move(self, moves, player, epsilon, debug):
        return self.explore_exploit(moves, player, epsilon, debug)

    # helps generate a move for the second player (will ultimately use the explore-exploit method in learning phase)
    def make_agent2_move(self, moves, player, epsilon,debug):
        return self.explore_exploit(moves, player, epsilon, debug)

    # returns the average absolute change in the value of a state
    def check_convergence(self):
        sum = 0.0
        count = 0
        for state in self.states.keys():
            current_value = self.states[state]
            if state in self.old_states:
                old_value = self.old_states[state]
            else:
                old_value = 0
            #change_fraction = abs(current_value-old_value)/(old_value + .00001)
            change = abs(current_value-old_value)

            sum += change
            count += 1
            self.old_states[state] = current_value
        #average_change = sum / count
        return sum
    # creates a value histogram
    def print_state_stats(self,plot=False,save_path=None):
        no_of_states = len(self.states.keys())
        print(f'No of states = {no_of_states}')

        if plot :
            self.states.pop('[0, 0, 0, 0, 0, 0, 0, 0, 0]', None)
            values = self.states.values()
            plt.hist(values,10)
            plt.title('Value Histogram')
            plt.xlabel('Value')
            plt.ylabel('# Of States')
            if save_path:
                plt.savefig(save_path)
            plt.show()
        '''
        for k,v in self.state_stats.items():
            if v < 50:
                print(f'{k} -> {v}')
        '''
        #self.state_stats.pop('[0, 0, 0, 0, 0, 0, 0, 0, 0]')
        #values = self.state_stats.values()
        #print(values)
        '''
        plt.hist(values,20)
        plt.title('Coverage Histogram')
        plt.xlabel('#no of games')
        plt.ylabel('# Of States')
        plt.show()
        '''
    # creates a convergence plot and how it decreases through the increase of iterations
    def print_converge_stats(self,save_path=None):
        x_axis = []
        y_axis = []
        for iter, change in self.convergence_stats:
            x_axis.append(iter/1000)
            y_axis.append(change)

        plt.plot(x_axis, y_axis)
        plt.title('Convergence Plot')
        plt.xlabel('No of Iterations In Thousands')
        plt.ylabel('Absolute Value Change')
        if save_path:
            plt.savefig(save_path)
        plt.show()


    def learn_one_game_modified(self):
        state_sequence=[]
        for move_no in range(9):
            if move_no % 2 == 0:
                player = 'X'
                agent1 = True
            else:
                player = 'O'
                agent1 = False
            moves = self.board.get_moves()
            current_state = self.board.get_state()
            state_sequence.append(current_state)

            if agent1:
                self.make_agent1_move(moves, player, 0.5, False)
            else:
                self.make_agent2_move(moves, player, self.epsilon,False)

            next_state = self.board.get_state()

            value = self.board.check_win_loss_draw()
            #print(f'value = {value}')
            if value == 1:
                #print('Player 1 wins')
                self.states[next_state] = 1
            elif value == -1:
                #print('Player 2 wins')
                self.states[next_state] = -1
            elif value == 0:
                #print('Its a draw')
                self.states[next_state] = 0
            #self.update_state_value(current_state, next_state)
            if value == 1 or value == -1 or value == 0:
                state_sequence.append(next_state)
                break
        #self.board.print_board()
        for i in range(len(state_sequence)-1,0,-1):
            next_state = state_sequence[i]
            current_state = state_sequence[i-1]
            self.update_state_value(current_state, next_state)

        self.board.reset_board()
    # Simulates one game
    def learn_one_game(self):
        for move_no in range(9):
            if move_no % 2 == 0:
                player = 'X'
                agent1 = True
            else:
                player = 'O'
                agent1 = False
            moves = self.board.get_moves()
            current_state = self.board.get_state()

            if agent1:
                self.make_agent1_move(moves, player,.5,False)
            else:
                self.make_agent2_move(moves, player, self.epsilon,False)

            next_state = self.board.get_state()

            value = self.board.check_win_loss_draw()
            #print(f'value = {value}')
            if value == 1:
                #print('Player 1 wins')
                self.states[next_state] = 1
            elif value == -1:
                #print('Player 2 wins')
                self.states[next_state] = -1
            elif value == 0:
                #print('Its a draw')
                self.states[next_state] = 0
            self.update_state_value(current_state, next_state)
            if value == 1 or value == -1 or value == 0:
                break
        #self.board.print_board()
        self.board.reset_board()
    # Simulates multiple games for the learning phase
    def learn_N_games(self, n_games, histogram_path=None, convergence_path=None):
        threshold = .01
        check_interval = 10000
        for i in range(n_games):
            self.learn_one_game_modified()
            if (i+1) % check_interval == 0:
                change = self.check_convergence()
                found_states = len(self.states.keys())
                print(f'Iter {i} found_states= {found_states} change={change} learning_rate={self.learning_rate}')
                self.convergence_stats.append((i+1,change))
                self.learning_rate *= .98
                self.print_state_stats()
        self.print_state_stats(True, save_path=histogram_path)
        self.print_converge_stats(save_path=convergence_path)

        #missing states
        fname = 'all-reached-states.pickle'
        with open(fname, 'rb') as f:
            all_states = pickle.load(f)

        for s in all_states.keys():
            if s not in self.states:
                print(f'Missing state {s}')



    #saves the game state
    def save_game_state(self,fname):
        with open(fname, 'wb') as f:
            pickle.dump(self.states, f)
    #restores the game state
    def restore_game_state(self,fname):
        with open(fname, 'rb') as f:
            self.states = pickle.load(f)
    # simulates a game for the testing phase (human vs computer) after the computer undergoes the learning phase
    def manual_play_one_game(self):
        for move in range(9):
            if move % 2 == 0:
                row = int(input("Enter a row:"))
                column = int(input("Enter a column:"))
                player = 'X'
                self.board.make_move(row, column, player)
            else:
                player = 'O'
                moves = self.board.get_moves()
                self.make_agent2_move(moves, player, 0, True)
            self.board.print_board()
            value = self.board.check_win_loss_draw()
            if value == 1:
                print('Player 1 wins')
                break
            elif value == -1:
                print('Player 2 wins')
                break
            elif value == 0:
                print('Its a draw')
    # simulates multiple games of the testing phase
    def manual_play_N_games(self, n_games):
        for i in range(n_games):
            self.manual_play_one_game()
            self.board.reset_board()


    def auto_play_one_game(self,agent1_epsilon,agent2_epsilon):
        for move_no in range(9):
            if move_no % 2 == 0:
                player = 'X'
                agent1 = True
            else:
                player = 'O'
                agent1 = False
            moves = self.board.get_moves()
            current_state = self.board.get_state()

            if agent1:
                self.make_agent1_move(moves, player,agent1_epsilon,False)
            else:
                self.make_agent2_move(moves, player, agent2_epsilon,False)

            next_state = self.board.get_state()

            value = self.board.check_win_loss_draw()
            #print(f'value = {value}')
            if value == 1:
                self.win1 +=1
            elif value == -1:
                self.win2 +=1
            elif value == 0:
                self.draw +=1
            if value == 1 or value == -1 or value == 0:
                break
        self.board.reset_board()

    def auto_play_N_games(self, n_games,agent1_epsilon,agent2_epsilon):
        for i in range(n_games):
            self.auto_play_one_game(agent1_epsilon,agent2_epsilon)
        print(f'Played={n_games} eps1={agent1_epsilon} eps2={agent2_epsilon} win1={self.win1} win2={self.win2} draw={self.draw}')
        win1, win2, draw = self.win1, self.win2, self.draw
        self.win1=self.win2=self.draw=0
        return win1, win2, draw



# main method to test the Game class
if __name__ == '__main__':
    num_games = 500000
    board = Board.Board()
    board.print_board()
    game = Game(board)
    # learns when learn = True and testing phase when learn = False
    learn = False
    if learn:
        game.learn_N_games(num_games)
        game.save_game_state('RL_TIC_TAC.pickle')

    else:
        game.restore_game_state('RL_TIC_TAC.pickle')
        game.auto_play_N_games(10000,.5,0)
        game.auto_play_N_games(10000,.4,0)
        game.auto_play_N_games(10000,.3,0)
        game.auto_play_N_games(10000,.2,0)
        game.auto_play_N_games(10000,.1,0)
        game.auto_play_N_games(10000,0,0)