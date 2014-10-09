
RED = 1;
BLACK = 2;
PLAYABLE = 0;
BOARDWIDTH=5;
BOARDHEIGHT=6;
K=4;
S_DEPTH=2;

def newBoard():
	return [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]];

verticalWins = [];
for(i = 0; i < 7; i++){
		for(var j = 0; j <= 6-4; j++){
			var win = [];
			for(var k = 0; k < 6; k++){
				win[k] = 0;
			}
			win[i] = 0xF<<j;
			//1111, 
			toRet.push(win);
		}
	}
	return toRet;
})();

def main():
	print newBoard();

if __name__ == "__main__": main()