var _ = require('lodash');
var util = require('util');

//maximizing red. board heights over 32 get fucky.
var  RED = 1, BLACK = 2, PLAYABLE=0, BOARDWIDTH=7,BOARDHEIGHT=6, S_DEPTH=3, K=4;

// columns, with bitfield rows
var newBoard = function(){
	return [_.times(BOARDWIDTH, function(){ return 0;}),
	        _.times(BOARDWIDTH, function(){ return 0;})];
}

//AND the win to zero out irrelavent bits, 
// and then and then OR with the NOT of the win, to see if there are holes in the thing you're testing
//wins are
var verticalWins = function(winlen){
	var toRet = [];
	for(var i = 0; i < BOARDWIDTH; i++){
		for(var j = 0; j <= BOARDHEIGHT-winlen; j++){
			var win = [];
			for(var k = 0; k < BOARDWIDTH; k++){
				win[k] = 0;
			}
			win[i] = ((1<<winlen)-1)<<j;
			
			toRet.push(win);
		}
	}
	return toRet;
};

var horizontalWins = function(winlen){
	var toRet = [];
	for(var j = 0; j < BOARDHEIGHT; j++){
		for(var i = 0; i <= BOARDWIDTH-winlen; i++){
			var win = [];
			for(var k = 0; k < BOARDWIDTH; k++){
				win[k] = 0;
			}
			for(var k = i; k < i+winlen; k++){
				win[k] = 0x1<<j; 1
			}
			toRet.push(win);
		}
	}
	return toRet;
};


var diagonalWins = function(winlen){
	var toRet = [];
	for(var i = 0; i <= BOARDWIDTH-winlen; i++){
		for(var j = 0; j <= BOARDHEIGHT-winlen; j++){
			var win = [];
			for(var k = 0; k < BOARDWIDTH; k++){
				win[k] = 0;
			}
			for(var k = 0; k < winlen; k++){
				win[i+k] = 0x1<<j+k;
			}
			toRet.push(win);
		}
	}
	for(var i = 0; i <= BOARDWIDTH-winlen; i++){
		for(var j = BOARDHEIGHT-1; j >= winlen-1; j--){
			var win = [];
			for(var k = 0; k < BOARDWIDTH; k++){
				win[k] = 0;
			}
			for(var k = 0; k < winlen; k++){
				win[i+k] = 0x1<<j-k;
			}
			toRet.push(win);
		}
	}
	return toRet;
};
var allWins = [].concat(horizontalWins(K), verticalWins(K), diagonalWins(K));
//console.log(allWins);

//AND the win to zero out irrelavent bits, 
//and then OR with the NOT of the win, to see if there are holes in the thing you're testing
var getState = function(board){
	outer: for(var j = 0; j < allWins.length; j++){
		win = allWins[j];
		var won = RED;
		for(var i = 0; i< board[0].length; i++){
			//console.log("checking "+ i);
			if( ((board[0][i]&win[i]) | (~win[i])) != -1){
				//console.log('black won')
				//console.log('board[0][i]:'+board[0][i])
				//console.log('win[i]:'+win[i])
				//console.log('(board[0][i]&win[i]):'+(board[0][i]&win[i]))
				won = BLACK;
				break;
			}
		}
		if(won == RED){
			//console.log("red won with: " + win);
			return RED;
		}
		for(var i = 0; i< board[1].length; i++){
			if( ((board[1][i]&win[i]) | (~win[i])) != -1)
				continue outer;
		}
		return BLACK;
	}
	return PLAYABLE;
}

//tests(); return;
var copyBoard = function(board){
	return [board[0].slice(),board[1].slice()];
}

var dropIn = function(i, board, toMove){
	//figure out where i would land
	var toLand = (board[0][i]|board[1][i])+1 // should be 1,2,4,8,16,32
	if(!(toLand == 1 || toLand == 2 || toLand == 4 || toLand == 8 || toLand == 16 || toLand == 32))
		console.log("you done goofd: "+toLand), process.exit(1);

	board[toMove-1][i] = board[toMove-1][i] | toLand
}

var printBoard = function(board){
	for(var i = BOARDHEIGHT; i-->0;){
		console.log('|'+
			_.zip(board[0].map(function(e){
				return (e&(1<<i))>>>i;
			}),
			board[1].map(function(e){
				return (e&(1<<i))>>>i;
			})).map(function(c){
				return c[0]?'r':c[1]?'b':' ';
			}).join('|')+'|');
	}
	console.log('['+board[0]+'],['+board[1]+']');
};

//if we do different color moves first, encode that too
//hash really is 
var getHash = function(board){
	var hashNum11 = board[0][0] |
	                board[0][1] << 6 | 
	                board[0][2] << 12 | 
	                board[0][3] << 18 | 
	                board[0][4] << 24;
	var hashNum12 = board[0][5] |
	                board[0][6] << 6 ;

	var hashNum21 = board[1][0] |
	                board[1][1] << 6 | 
	                board[1][2] << 12 | 
	                board[1][3] << 18 | 
	                board[1][4] << 24;
	var hashNum22 = board[1][5] |
	                board[1][6] << 6 ;
	return (((''+hashNum11)+hashNum12)+hashNum21)+hashNum22;
}

var other = function(playnum){
	return playnum==RED?BLACK:RED
}
var andZipper = function(e){
	return e[0]&e[1];
}
var xorZipper = function(e){
	return e[0]^e[1];
}
var oneBits = function(n){
	return Number(n).toString(2).replace(/0/g,'').length;
}
var heuristic = function(board){
	//one side only
	//console.log("huering board: ")
	//printBoard(board);
	var ans = allWins.reduce(function(p,win){
		zerodBoard = _.zip(win,board[0]).map(andZipper);
		holes = _.zip(win,zerodBoard).map(xorZipper);
		//score = (winlen-#holes) / winlen
		var filled = (K-holes.reduce(function(p,c){return p+oneBits(c);},0))
		score = filled*filled*filled*filled / K;
		if(_.zip(holes,board[1]).map(andZipper).reduce(function(p,c){return p&&(c==0);},true)){
			return p+score;
		}
		return p;
	},0) 
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
//allWins = [allWins[0]];
console.log(heuristic([[0,0,1,1,0,0,0],[0,0,0,0,0,0,0]]))

//return;

var counter = 0;
var boardMap = {};
var play = function(node,depth){
	//console.log(counter++);
	var hash = getHash(node.board)
	node.state = getState(node.board);
	//console.log('playing board:');
	//printBoard(node.board);
	//console.log(node.board+'');
	//console.log('======');

	if(boardMap[hash] == undefined)
		boardMap[hash] = node;
	else {
		return boardMap[hash];
	}
	if(node.state != PLAYABLE){
		(++counter);
		//printBoard(node.board);
		node.favorability = node.state==RED?2147483647:-2147483648;
		return node;
	}
	if(depth == 0){
		node.favorability = heuristic(node.board);
		return node;
	}
	node.children = [];
	for(var i = 0; i< BOARDWIDTH; i++){
		if((node.board[0][i]|node.board[1][i]) == ((1<<BOARDHEIGHT)-1)){ // slot is full
			continue;}
		var nextBoard = copyBoard(node.board);
		dropIn(i,nextBoard,node.toMove);
		node.children[i] = play({
			board: nextBoard,
			children: [],
			toMove: other(node.toMove)
		},depth-1);
		//if one of the children won
	}
	//console.log('doneplayin chinlis: '+node.children);
	node.favorability = node.children.length == 0?0:
	node.children.reduce(function(p,child){
		return (node.toMove==RED?Math.max:Math.min)(p,child.favorability);
	},(node.toMove==RED?-2147483647:2147483647));
	//console.log("recursing up:" +node.blackWins+", "+node.redWins);
	//console.log(util.inspect(node.board,{colors: true}));
	return node;
}


var gameTree = {
	board: newBoard(),
	state: PLAYABLE,
	children: [],
	toMove: RED,
}

var gameTree = play(gameTree,S_DEPTH);
//console.log(util.inspect(gameTree,{colors: true}));
//console.log('found win: '+counter);
//now play the game

//I move. pick best child.
var nextGameTree;
for(var i = 0; i < BOARDWIDTH; i++){
	if(gameTree.children[i] == undefined)
		continue;
	if(nextGameTree == undefined)
		nextGameTree = gameTree.children[i];
	else
		nextGameTree = nextGameTree.favorability>gameTree.children[i].favorability?nextGameTree:gameTree.children[i];
}
gameTree = nextGameTree;
var board = gameTree.board
console.log('Computer moved. board looks like this:')
printBoard(board);
var playGame = function() {
	var chunk = process.stdin.read();
	if (chunk !== null) {
		column = parseInt(chunk);
		if(column>=BOARDWIDTH||column<0 || 
			(board[0][column]|board[1][column]) == (1<<BOARDHEIGHT)-1){
			console.log("Move correctly, fucker.");
			return;
		}
		dropIn(column, board, BLACK);
		console.log('You moved in column '+column+'. board looks like this:')
		printBoard(board);
		if(getState(board)==BLACK){
			console.log("BLACK WINS");
			process.exit(0);
		}
		//player moved, pare tree
		/*for(var i = 0; i < gameTree.children.length; i++){
			console.log('board '+i+':');
			printBoard(gameTree.children[i].board);
		}*/
		gameTree = gameTree.children[column];
		//I move. pick best child.
		boardMap = {};
		gameTree = play({
			board: board,
			state: PLAYABLE,
			children: [],
			toMove: RED,
		},S_DEPTH)
		//play then pick
		console.log('children.length: '+ gameTree.children.length);
		var nextGameTree;
		for(var i = 0; i < BOARDWIDTH; i++){
			if(gameTree.children[i] == undefined)
				continue;
			if(nextGameTree == undefined)
				nextGameTree = gameTree.children[i];
			else
				nextGameTree = nextGameTree.favorability>gameTree.children[i].favorability?nextGameTree:gameTree.children[i]
		}

		board = nextGameTree.board
		console.log('Computer moved. board looks like this:')
		printBoard(board);
		if(getState(board)==RED){
			console.log("RED WINS");
			process.exit(0);
		}
	}
}
process.stdin.on('readable', playGame);

function tests(){
//var allWins = [].concat(horizontalWins(K));
//var allWins = [].concat(verticalWins(K));
//var allWins = [].concat(diagonalWins(K));
	if(getState([[0,2,4,0,8,16,16],[4,8,0,0,4,8,16]]) != 2)
		console.log("fail");
	if(getState([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]) != 0)
		console.log("fail");
}
