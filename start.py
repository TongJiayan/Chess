import chess
import book

book.LoadOpeingBook()
board = chess.Board()

import AI
import boardset

# str=input("input: \n")
# print(str)

#print(board)

# 使用dict来初始化board_info
# 其中主要有black_queens,black_rooks,white_materials,white position,black_position,hash值，相当于将以下变量打包
board_info={} 
boardset.board_start(board, board_info)
color = input()#("\nBlack/White:")		

var = 1
if color=="white":
	board_info['color_AI'] = 1
	while var == 1:
		str_san = AI.do_search(board, board_info)
		boardset.board_info_set(board, str_san, board_info)
		board_info['hash'] = chess.polyglot.zobrist_hash(board)
		print(str_san)
		board.push_san(str_san)
		#print("\nAI:\n")
		#print(board)

		#san_list = []
		#for n in board.legal_moves:
		#	san_list.append(board.san(n))
		
		str_my = input()#("\ninput: \n")
		#while 1 == 1:
		#	if str_my in san_list:
		#		break
		#	str_my = input("re-input: \n")

		boardset.board_info_set(board, str_my, board_info)
		board.push_san(str_my)
	
		
		#print("\nYOU:\n")
		#print(board)
		#if board.is_game_over():
		#	var=0
else:
	board_info['color_AI']=0
	while var == 1:
		#san_list = []
		#for n in board.legal_moves:
		#	san_list.append(board.san(n))
		#print("hahah:",san_list)
		str_my = input()#("\ninput: \n")
		#while 1 == 1:
		#	if str_my in san_list:
 		#		break
		#	str_my = input("re-input: \n")

		boardset.board_info_set(board, str_my, board_info)
		board.push_san(str_my)
	
		#print("\nYOU:\n")
		#print(board)
		

		str_san = AI.do_search(board, board_info)
		boardset.board_info_set(board, str_san, board_info)
		board_info['hash'] = chess.polyglot.zobrist_hash(board)
		print(str_san)
		board.push_san(str_san)
		#print("\nAI:\n")
		#print(board)


		#if board.is_game_over():
		#	var=0
