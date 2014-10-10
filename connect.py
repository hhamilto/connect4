#HASH TAG
import sys

RED = 1;
BLACK = 2;
PLAYABLE = 0;
BOARDWIDTH=6;
BOARDHEIGHT=6;
K=4;
S_DEPTH=2;

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
			break
		height=height+1
	board[i][height] = toMove

def printBoard(board):
	for i in xrange(1,BOARDHEIGHT+1):
		sys.stdout.write('|')
		for col in board:
			sys.stdout.write(('r' if col[BOARDHEIGHT-i]==RED else 'b' if col[BOARDHEIGHT-i]==BLACK else ' ')+'|')
		sys.stdout.write('\n')



def heuristic(board):
	#one side only
	#console.log("huering board: ")
	#printBoard(board);
	score = 0
	for win in allWins:
		filled = 0;
		for cell in win:
			if board[cell[0]][cell[1]] == RED:
				filled = filled+1
			elif board[cell[0]][cell[1]] == BLACK:
				filled = -K
		if filled > 0 :
			score = score + filled*filled*filled*filled / (K*1.0)#force floating point?
		zerodBoard = _.zip(win,board[0]).map(andZipper);
		holes = _.zip(win,zerodBoard).map(xorZipper);
		//score = (winlen-#holes) / winlen
		var filled = (K-holes.reduce(function(p,c){return p+oneBits(c);},0))
		score = filled*filled*filled*filled / K;
		if(_.zip(holes,board[1]).map(andZipper).reduce(function(p,c){return p&&(c==0);},true)){
			return p+score;
		}
		return p;
	},allWins,0) 
	- allWins.reduce(function(p,win){
		zerodBoard = _.zip(win,board[1]).map(andZipper);
		holes = _.zip(win,zerodBoard).map(xorZipper);
		//score = (winlen-#holes) / winlen
		var filled = (K-holes.reduce(function(p,c){return p+oneBits(c);},0))
		score = filled*filled*filled*filled / K;
		if(_.zip(holes,board[0]).map(andZipper).reduce(function(p,c){return p&&(c==0);},true)){
			return p+score;
		}
		return p;
	},0);
	//console.log(ans);
	return ans;
}


def main():
	#print allWins

	if True: #tests to make sure stuffs not fucked up
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

if __name__ == "__main__": main()