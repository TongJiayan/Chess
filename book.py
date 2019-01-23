import chess
import random
import chess.polyglot

OpeningBook_Dict = {}


#放在start.py中执行
def LoadOpeingBook():
    global OpeningBook_Dict
    f = open('data/open_dict.txt', 'r')
    a = f.read()
    OpeningBook_Dict = eval(a)
    f.close()

#搜索开局库
def book_move(board):
	board_hash = hex(chess.polyglot.zobrist_hash(board))
	if board_hash in OpeningBook_Dict:
		choosable_moves = list(OpeningBook_Dict[board_hash].keys())
		move = choosable_moves[0]
	else:
		with chess.polyglot.open_reader("data/polyglot/performance.bin") as reader:
			try:
				move = board.san(reader.find(board).move())
			except IndexError:
				move = None
	return move

