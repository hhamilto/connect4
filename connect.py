#HASH TAG
import sys

RED = 1;
BLACK = 2;
PLAYABLE = 0;
BOARDWIDTH=7;
BOARDHEIGHT=6;
K=4;
S_DEPTH=5;

#boards are index by rows going 0 to right most then columns from 0 to top
def newBoard():
	newBoard = []
	for i in xrange(0, BOARDWIDTH):
		col = [];
		for j in xrange(0, BOARDHEIGHT):
			col.append(PLAYABLE)
		newBoard.append(col)
	return newBoard

def verticalWins():
	toRet = []
	for i in xrange(0, BOARDWIDTH):
		for j in xrange(0, BOARDHEIGHT-K+1):
			win = [];
			for k in xrange(0, K):
				win.append([i,j+k])
			toRet.append(win)
	return toRet

def horizontalWins():
	toRet = []
	for i in xrange(0, BOARDHEIGHT):
		for j in xrange(0, BOARDWIDTH-K+1):
			win = [];
			for k in xrange(0, K):
				win.append([j+k,i])
			toRet.append(win)
	return toRet

def diagonalWins():
	toRet = []
	for i in xrange(0, BOARDWIDTH-K+1):
		for j in xrange(0, BOARDHEIGHT-K+1):
			win = [];
			for k in xrange(0, K):
				win.append([i+k,j+k])
			toRet.append(win)
	for i in xrange(0, BOARDWIDTH-K+1):
		for j in xrange(K-1,BOARDHEIGHT):
			win = [];
			for k in xrange(0, K):
				win.append([i+k,j-k])
			toRet.append(win)
	return toRet

allWins = verticalWins()+horizontalWins()+diagonalWins();
#allWins = horizontalWins()

def getState(board):
	for win in allWins:
		try:
			color = board[win[0][0]][win[0][1]];
			if color != PLAYABLE:
				for spot in win[1:]:
					if board[spot[0]][spot[1]] != color:
						raise StopIteration
				return color
		except StopIteration:
			"continue"
	return PLAYABLE

def copyBoard(board):
	newBoard = []
	for col in board:
		newBoard.append(col[:])
	return newBoard

def dropIn(i, board, toMove):
	#figure out where i would land
	height = 0
	for cell in board[i]:
		if cell == 0:
			break #We found and open space
		height=height+1
	board[i][height] = toMove

def printBoard(board):
	for i in xrange(1,BOARDHEIGHT+1):
		sys.stdout.write('|')
		for col in board:
			sys.stdout.write(('r' if col[BOARDHEIGHT-i]==RED else 'b' if col[BOARDHEIGHT-i]==BLACK else ' ')+'|')
		sys.stdout.write('\n')


# so this thing guestimates how "good" a board is
def heuristic(board):
	score = 0
	#compute red's  "goodness" or advantage
	for win in allWins:
		filled = 0;
		for cell in win:
			if board[cell[0]][cell[1]] == RED:
				filled = filled+1
			elif board[cell[0]][cell[1]] == BLACK:
				filled = -K #if black is blocking, don't fuck with the score
		if filled > 0 :
			score = score + filled*filled*filled*filled / (K*1.0)#force floating point?
	#subtract good positions for black
	for win in allWins:
		filled = 0;
		for cell in win:
			if board[cell[0]][cell[1]] == BLACK:
				filled = filled+1
			elif board[cell[0]][cell[1]] == RED:
				filled = -K
		if filled > 0 :
			score = score - filled*filled*filled*filled / (K*1.0)#force floating point?
	return score;

def other(color):
	return RED if color==BLACK else BLACK

def play(node,depth):
	node["state"] = getState(node["board"]);

	#print "hello"
	if node["state"] != PLAYABLE :
		node["favorability"] = 2147483647 if node["state"]==RED else -2147483647; #red win is good, black win is bad
		return node;

	if depth == 0:
		node["favorability"] = heuristic(node["board"]);
		return node;

	#print "hello"
	node["children"] = [];
	for i in xrange(BOARDWIDTH):
		if node["board"][i][BOARDHEIGHT-1] != 0: #slot is full
			continue
		nextBoard = copyBoard(node["board"])
		dropIn(i,nextBoard,node["toMove"]);
		#print "makin kids"
		node["children"].append(play({ "board": nextBoard, "toMove": other(node["toMove"]) },depth-1));

	#print "hello"

	if node["toMove"] ==RED: #red picks the best move
		maxVal = -2147483600
		for child in node["children"]:
			if child["favorability"] > maxVal:
				maxVal = child["favorability"]
		node["favorability"] = maxVal
	elif node["toMove"] == BLACK: #black picks shittiest move for red
		minVal = 2147483600
		for child in node["children"]:
			if child["favorability"] < minVal:
				minVal = child["favorability"]
		node["favorability"] = minVal
	else:
		print "fuck." #fucked up

	return node;


def main():
	#print allWins
	board = newBoard();
	while True:
		gameTree = play({ "board": board, "toMove": RED },S_DEPTH);
		#computer picks best move
		best = gameTree["children"][0]
		for child in gameTree["children"]:
			if child["favorability"] > best["favorability"]:
				best = child
		board = best["board"]
		print "Computer moved:"
		printBoard(board)
		print "Enter column to drop your piece in: (1 indexed)"
		column = 0
		while column == 0:
			try:
				column = int(raw_input())
			except ValueError:
				print 'Invalid Number'
				column = 0
		dropIn(column-1, board, BLACK);
		printBoard(board)

	if False: #tests to make sure stuffs not fucked up
		print getState([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) == 0
		print getState([[1,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) == 1
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[0,0,0,2,0,0],[0,0,0,2,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) == 2
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[0,0,0,0,0,0],[0,0,0,2,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) == 0
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[0,0,0,1,0,0],[0,0,1,2,0,0],[0,1,0,0,0,0],[1,0,0,0,0,0]]) == 1
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[0,0,2,1,0,0],[0,0,0,2,0,0],[0,1,0,0,2,0],[1,0,0,0,0,2]]) == 2
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[0,0,2,1,0,0],[0,0,0,2,0,0],[0,1,0,0,2,0],[1,0,1,1,1,1]]) == 1
		print getState([[1,1,1,2,0,0],[0,0,0,2,0,0],[2,0,2,1,0,0],[0,2,0,2,0,0],[0,1,2,0,2,0],[1,0,1,2,1,1]]) == 2
		print getState([[1,1,1,2,0,1],[0,0,0,2,1,0],[2,0,2,1,0,0],[0,2,1,2,0,0],[0,1,2,0,2,0],[1,0,1,0,1,1]]) == 1
		print getState([[1,1,1,2,0,1],[0,0,0,2,1,0],[2,0,2,1,0,0],[0,2,0,2,0,0],[0,1,2,0,2,0],[1,0,1,0,1,1]]) == 0
		board = newBoard();
		dropIn(0,board,RED)
		dropIn(0,board,RED)
		dropIn(0,board,RED)
		dropIn(2,board,BLACK)
		dropIn(2,copyBoard(board),BLACK)
		print board == [[1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

		print heuristic([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) == 0
		print heuristic([[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) > 0
		print heuristic([[1,1,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) > heuristic([[1,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
		print heuristic([[1,1,2,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]) < heuristic([[1,1,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[2,0,0,0,0,0]])
if __name__ == "__main__": main()