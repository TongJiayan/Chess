import chess
import book
import boardset
import TableF
def sort_moves(board, moves):
	...


#board.turn white=true    去掉ply
# board_info
# search
# result
def root_search(Search *search, board, depth, int ply, alpha, beta, Move *result):
	...






bb.board_start(board, board_info)

def do_search(board, board_info):
	(is_get, san) = book_move(board, board_info)
	if is_get == 1:
		return 1, san or move\???.................................................


	#接下来是在开局库中找不到的情况



	# search->stop = 0;
    result = 1;

    #用类来定义结构体  table在一次走棋中用一次就要删除！
    #do_search也只执行一次
    table = Gfunction.Table
    Gfunction.table_alloc(table, 20)
    # table_alloc(&search->table, 20)

    # double start = now();
    # double duration = search->duration;
    # if (duration > 0) {
    #     thread_start(search);
    # }
    score = 0
    for depth in range(1:3):
    	lo = 20
    	hi = 20
    	while 1 == 1:
    		alpha = score - lo
    		beta = score + hi
    		score = root_search(search, board, depth, 0, alpha, beta, &search->move)\..................................
    		# if (search->stop) {
      #           break;
      #       }
            if score == alpha: 
                lo *= 5
            elif score == beta:
                hi *= 5
            else:
                break

        # if (search->stop) {
        #     break;
        # }
        if score == -INF:\..............................................
            result = 0
            break
        # double elapsed = now() - start;
        # if (duration > 0 && elapsed > duration) {
        #     break;
        # }
        if (score <= -MATE + depth) or (score >= MATE - depth):
            break
     
    # if (now() - start < 1) {
    #     sleep(1);
    # }
    move_to_san
    # table_free(&search->table);
    return result,san\......................................................

