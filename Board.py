
import random
import pickle

class Board:
# initializes board and other aspects of the board
    def __init__(self):
        self.board=[ [0]*3 for i in range(3)] # Board as a 2-D array of 3 rows and 3 columns
    # Returns the legal moves that an opponent can make
    def get_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    moves.append(tuple((i, j)))
        return moves
    # makes the moves for a certain player at a specific row and column
    def make_move(self, row, col, player):
        if self.board[row][col] != 0:
            return False
        if player == 'X':
            self.board[row][col] = 1
        else:
            self.board[row][col] = -1
        return True
    # resets the move to a blank position
    def reset_move(self, row, col):
        self.board[row][col] = 0
    # returns a string representation of the current state
    def get_state(self):
        states_list = []
        for i in range(3):
            for j in range(3):
                states_list.append(self.board[i][j])
        return str(states_list)

    # prints the board as a string
    def print_board(self):
        for i in range(3):
            print(f'{self.board[i][0]} {self.board[i][1]} {self.board[i][2]}')
    # resets the board to its original state
    def reset_board(self):
        self.board = [ [0]*3 for i in range(3)]

    # checks whether the game is a win, loss, or draw for the player (player makes the first move 'X')
    def check_win_loss_draw(self):
        isOver = False
        value = -100
        WIN = 1
        LOSS = -1
        DRAW = 0
        # check rows
        for i in range(3):
            sum = 0
            for j in range(3):
                sum += self.board[i][j]
            if sum == 3:
                isOver = True
                value = WIN
                break
            if sum == -3:
                isOver = True
                value = LOSS
                break

        # check columns
        for i in range(3):
            sum2 = 0
            for j in range(3):
                sum2 += self.board[j][i]
            if sum2 == 3:
                isOver = True
                value = WIN
                break
            if sum2 == -3:
                isOver = True
                value = LOSS
                break
        sum3 = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if sum3 == 3:
            isOver = True
            value = WIN
        if sum3 == -3:
            isOver = True
            value = LOSS

        sum4 = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if sum4 == 3:
            isOver = True
            value = WIN
        if sum4 == -3:
            isOver = True
            value = LOSS
        if isOver is False and len(self.get_moves()) == 0:
            value = DRAW
        return value
# simulates a random game of Tic Tac Toe
def play_random_game(board):
    for move_no in range(9):
        if move_no % 2 == 0:
            player = 'X'
        else:
            player = 'O'

        moves = board.get_moves()
        (row, column) = random.choice(moves)

        print(f'making move for player {player} {row} {column}')
        board.make_move(row, column, player)
        value = board.check_win_loss_draw()
        print(f'value = {value}')
        if value == 1:
            print('Player 1 wins')
            break
        elif value == -1:
            print('Player 2 wins')
            break
        elif value == 0:
            print('It is a draw')
        else:
            print('Make more moves')
    board.print_board()

player1_win =0
player2_win =0
draw =0

states = {}
def play_moves_recur(board,level):
    global player1_win, player2_win, draw
    global states

    if level > 9:
        return

    if level %2 == 0:
        player='X'
    else:
        player = 'O'

    moves = board.get_moves()
    for row, column in moves:
        board.make_move(row, column, player)
        state = board.get_state()
        states[state] = 1
        value = board.check_win_loss_draw()
        #print(f'value = {value}')
        if value == 1:
            player1_win +=1
        elif value == -1:
            player2_win +=1
        elif value == 0:
            draw +=1
        else:
            play_moves_recur(board,level+1)
        board.reset_move(row,column)



# main function for testing the Board class
if __name__ == '__main__':
    board = Board()
    board.print_board()

    #play_random_game(board)
    #print(board.get_state())

    play_moves_recur(board,0)
    print(f'win1={player1_win} win2={player2_win} draw={draw}')
    reached_states = len(states.keys())
    print(f'states = {reached_states}')

    fname = 'all-reached-states.pickle'
    with open(fname, 'wb') as f:
        pickle.dump(states, f)

    '''
    print(board.get_moves())
    board.make_moves(1, 1, 'O')
    board.make_moves(2, 1, 'O')
    board.make_moves(0, 2, 'X')
    print(board.get_moves())
    board.make_moves(2, 0, 'O')
    board.make_moves(2, 2, 'X')
    board.make_moves(1, 2, 'X')
    board.print_board()
    print(board.get_moves())
    value= board.check_win_loss_draw()
    if value == 3:
        print('Player 1 wins')
    elif value == -3:
        print('Player 2 wins')
    elif value == 0:
        print('Its a draw')
    else:
        print('Make more moves')
    '''



