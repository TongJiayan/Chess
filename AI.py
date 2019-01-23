import chess
import Gfunction
import TableF
import copy
import chess.polyglot
import boardset
import book

TABLE_NONE = 0
TABLE_EXACT = 1
TABLE_ALPHA = 2
TABLE_BETA = 3
# 比方说你在评价域中保存了16，并且在标志域保存了“hashfEXACT”，这就意味着该结点的评价是准确值16；
# 如果你在标志域中保存了“hashfALPHA”，那么结点的值最多是16；如果保存了“hashfBETA”，这个值就至少是16。
INFI = 500000
search_time = 20


def sorted_legal_san(board, san_list):
    # 找出所有走法，并按得分降序装入列表
    san_list_all = []
    for n in board.legal_moves:
        san_list_all.append(board.san(n))
    # print(san_list_all)
    san_dict = {}  # 存放当前board下，所有着子的得分
    for i in san_list_all:
        san_dict[i] = boardset.score_san(board, i)

    # 对san_dict进行排序
    san_value_list = sorted(san_dict.items(), key=lambda item: item[1], reverse=True)

    for i in san_value_list:
        san_list.append(i[0])  # i[0]:走子，如Nh3 i[1]:得分
    return


# 生成杀棋，用于静态搜索
def gen_sorted_capture_move(board, capture_san_list):
    capture_list = []
    for i in board.legal_moves:
        if board.is_capture(i):
            capture_list.append(board.san(i))

    san_dict = {}
    for i in capture_list:
        san_dict[i] = boardset.score_san(board, i)

    san_value_list = sorted(san_dict.items(), key=lambda item: item[1], reverse=True)

    for i in san_value_list:
        capture_san_list.append(i[0])
    return


def quiesce(board, board_info, alpha, beta):
    # if board.is_checkmate():
    #     return AlphaBeta(board, board_info, table, alpha, beta, 1);
    # 加上将军判断会导致一直递归

    value = evaluate(board, board_info)
    if value >= beta:
        return beta
    if value > alpha:
        alpha = value

    capture_san_list = []
    gen_sorted_capture_move(board, capture_san_list)
    for i in capture_san_list:
        board_info_temp = copy.deepcopy(board_info)
        boardset.board_info_set(board, i, board_info_temp)
        board.push_san(i)
        board_info_temp['hash'] = chess.polyglot.zobrist_hash(board)
        value = -quiesce(board, board_info_temp, -beta, -alpha)
        board.pop()
        del board_info_temp
        if value >= beta:
            return beta
        if value > alpha:
            alpha = value

    return alpha


def AlphaBeta(board, board_info, table, alpha, beta, depth):
    fFoundPv = False
    # 在Alpha-Beta搜索中，任何结点都属于以下三种类型：
    # 1. Alpha结点。每个搜索都会得到一个小于或等于Alpha的值，这就意味着这里没有一个着法是好的，可能是因为这个局面对于要走的一方太坏了。
    # 2. Beta结点。至少一个着法会返回大于或等于Beta的值。
    # 3. 主要变例(PV)结点。有一个或多个着法会返回大于或等于Alpha的值(即PV着法)，但是没有着法会返回大于或等于Beta的值。
   
    # 在置换表中寻找了，可以直接返回
    board_hash = board_info['hash']
    (is_get, value) = TableF.table_get(table, board_hash, depth, alpha, beta)
    if is_get:
        return value

    # 递归到底层 返回分数
    if depth <= 0:
        # value = evaluate(board, board_info)
        value = quiesce(board, board_info, alpha, beta)
        # 把算好的值存到置换表中
        TableF.table_set(table, board_info['hash'], depth, value, TABLE_EXACT)
        return value


    # do_null_move
    # 在一个实在着法之前，允许连续两个空着裁剪
    R=0
    if depth<=6 :
        R=2
    else:
        R=3

    if not board.is_checkmate(): 
        if board_info['null_move_pace']<2:
            null_move_san = board.san(chess.Move.null())
            board_info_temp = copy.deepcopy(board_info)
            board.push_san(null_move_san)
            board_info_temp['hash'] = chess.polyglot.zobrist_hash(board)
            board_info_temp['null_move_pace']+=1
            value = -AlphaBeta(board, board_info_temp, table, -beta, -beta + 1, depth - 1 - R)
            board.pop()
            del board_info_temp
            if value >= beta:
               TableF.table_set(table, board_info['hash'], depth, value, TABLE_BETA)
               return beta
        else:
            board_info['null_move_pace']=0

    # 死局，无棋可走
    if board.is_game_over():
        value = evaluate(board, board_info)
        return value

    san_list = []
    sorted_legal_san(board, san_list)



    # if len(san_list) == 0:
    #     value = -AlphaBeta(board, board_info, table, -beta, -alpha, 0)
    #     return value

    str = san_list[0]
    flag = TABLE_ALPHA

    for i in san_list:
        board_info_temp = copy.deepcopy(board_info)
        boardset.board_info_set(board, i, board_info_temp)
        board.push_san(i)
        board_info_temp['hash'] = chess.polyglot.zobrist_hash(board)
        # board_set(board, sq, piece, board_info):
        # 拷贝一份棋盘信息进行修改

        if fFoundPv:
            value = -AlphaBeta(board, board_info_temp, table, -alpha-1, -alpha, depth - 1)
            if (value > alpha) and (value < beta):
                # 检查失败
                value = -AlphaBeta(board, board_info_temp, table, -beta, -alpha, depth - 1)
        else:
            value = -AlphaBeta(board, board_info_temp, table, -beta, -alpha, depth - 1)
        
        board.pop()
        del board_info_temp

        if value >= beta:
            TableF.table_set(table, board_info['hash'], depth, beta, TABLE_BETA)
            return beta

        if value > alpha:
            alpha = value
            flag = TABLE_EXACT
            fFoundPv = True

    TableF.table_set(table, board_info['hash'], depth, alpha, flag)
    return alpha



def root_search(board, board_info, table, alpha, beta, depth):
    san_list = []
    sorted_legal_san(board, san_list)
    # san_list为空的时候已经被将死
    best_san = san_list[0]
    value = float('-inf')
    for i in san_list:
        board_info_temp = copy.deepcopy(board_info)
        boardset.board_info_set(board, i, board_info_temp)
        board.push_san(i)
        board_info_temp['hash'] = chess.polyglot.zobrist_hash(board)


        value = -AlphaBeta(board, board_info_temp, table, -beta, -alpha, depth - 1)
       

        board.pop()
        del board_info_temp

        if value > alpha:   
            alpha = value
            best_san = i

    # table_set_move()
    return alpha, best_san


def do_search(board, board_info):

    table = [0, 0, 0]
    TableF.table_alloc(table, 20)

    depth = 4
    final_san = ''
    value = float("-inf")     #value=-3000
    alpha = -INFI
    beta = INFI
    valWINDOW = 50

    cur_dep=1
    while cur_dep<depth:
        (temp_value, temp_final_san) = root_search(board, board_info, table, alpha, beta, cur_dep)
        if temp_value<=alpha:
            alpha =-INFI
            continue
        elif temp_value>=beta:
            beta =INFI
            continue
        else:
            if temp_value > value:
                value = temp_value
                final_san = temp_final_san
            alpha=value - valWINDOW
            beta=value + valWINDOW
            cur_dep+=1



    del table
    return final_san


value_table = [
    # pawn
    [0, 0, 0, 0, 0, 0, 0, 0,
     50, 50, 50, 50, 50, 50, 50, 50,
     10, 10, 20, 30, 30, 20, 10, 10,
     5, 5, 10, 25, 25, 10, 5, 5,
     0, 0, 0, 20, 20, 0, 0, 0,
     5, -5, -10, 0, 0, -10, -5, 5,
     5, 10, 10, -20, -20, 10, 10, 5,
     0, 0, 0, 0, 0, 0, 0, 0],

    # knight
    [-50, -40, -30, -30, -30, -30, -40, -50,
     -40, -20, 0, 0, 0, 0, -20, -40,
     -30, 0, 10, 15, 15, 10, 0, -30,
     -30, 5, 15, 20, 20, 15, 5, -30,
     -30, 0, 15, 20, 20, 15, 0, -30,
     -30, 5, 10, 15, 15, 10, 5, -30,
     -40, -20, 0, 5, 5, 0, -20, -40,
     -50, -40, -30, -30, -30, -30, -40, -50],

    # bishop
    [-20, -10, -10, -10, -10, -10, -10, -20,
     -10, 0, 0, 0, 0, 0, 0, -10,
     -10, 0, 5, 10, 10, 5, 0, -10,
     -10, 5, 5, 10, 10, 5, 5, -10,
     -10, 0, 10, 10, 10, 10, 0, -10,
     -10, 10, 10, 10, 10, 10, 10, -10,
     -10, 5, 0, 0, 0, 0, 5, -10,
     -20, -10, -10, -10, -10, -10, -10, -20],

    # rook
    [0, 0, 0, 0, 0, 0, 0, 0,
     5, 10, 10, 10, 10, 10, 10, 5,
     -5, 0, 0, 0, 0, 0, 0, -5,
     -5, 0, 0, 0, 0, 0, 0, -5,
     -5, 0, 0, 0, 0, 0, 0, -5,
     -5, 0, 0, 0, 0, 0, 0, -5,
     -5, 0, 0, 0, 0, 0, 0, -5,
     0, 0, 0, 5, 5, 0, 0, 0],

    # queen
    [-20, -10, -10, -5, -5, -10, -10, -20,
     -10, 0, 0, 0, 0, 0, 0, -10,
     -10, 0, 5, 5, 5, 5, 0, -10,
     -5, 0, 5, 5, 5, 5, 0, -5,
     0, 0, 5, 5, 5, 5, 0, -5,
     -10, 5, 5, 5, 5, 5, 0, -10,
     -10, 0, 5, 0, 0, 0, 0, -10,
     -20, -10, -10, -5, -5, -10, -10, -20],

    # king
    [-30, -40, -40, -50, -50, -40, -40, -30,
     -30, -40, -40, -50, -50, -40, -40, -30,
     -30, -40, -40, -50, -50, -40, -40, -30,
     -30, -40, -40, -50, -50, -40, -40, -30,
     -20, -30, -30, -40, -40, -30, -30, -20,
     -10, -20, -20, -20, -20, -20, -20, -10,
     20, 20, 0, 0, 0, 0, 20, 20,
     20, 30, 10, 0, 0, 10, 30, 20],
]

value_table_reversed = [table.copy() for table in value_table]
for table in value_table_reversed:
    table.reverse()

material_balance_value_table = [100, 320, 330, 500, 900, 20000]


def evaluate(board, board_info):
    # turn==  AI_COLOR  此时value不用取负
    value = 0
    if board.is_game_over():
        if board.result() == "1-0":
            # White win
            if board_info['color_AI']:
                value = INFI - 10
            else:
                value = -INFI + 10
        elif board.result() == "0-1":
            # Black win
            if board_info['color_AI']:
                value = -INFI + 10
            else:
                value = INFI - 10
        else:
            value = 0
        if not (board.turn == board_info['color_AI']):
            value = -value
        return value

    total_evaluationW=0
    total_evaluationB=0
    for i in chess.SQUARES:
        piece = board.piece_at(i)
        if piece is not None:
            if piece.color:
                total_evaluationW += value_table_reversed[piece.piece_type - 1][i]
                total_evaluationW += material_balance_value_table[piece.piece_type - 1]
            else:
                total_evaluationB += value_table[piece.piece_type - 1][i]
                total_evaluationB += material_balance_value_table[piece.piece_type - 1]
    hehe = 0.98
    if (board_info['color_AI'] == 1):
        total_evaluationB = int(hehe * total_evaluationB)
    else:
        total_evaluationW = int(hehe * total_evaluationW)

    if (board_info['color_AI'] == 1):
        value = total_evaluationW - total_evaluationB
    else:
        value = total_evaluationB - total_evaluationW

    # if board_info['color_AI'] == 1:  # AI执白棋
    #     value += board_info['white_material']
    #     value -= board_info['black_material']
    #     value += board_info['white_position']
    #     value -= board_info['black_position']
    # else:
    #     value -= board_info['white_material']
    #     value += board_info['black_material']
    #     value -= board_info['white_position']
    #     value += board_info['black_position']

    if not (board.turn == board_info['color_AI']):
        value = -value

    return value












##机动性评估
def mobility(board, color_AI):
    MobilityBonus = {"Knights": (-75, -57, -9, -2, 6, 14, 22, 29, 36), \
                     "Bishops": (-48, -20, 16, 26, 38, 51, 55, 63, 63, 68, 81, 81, 91, 98), \
                     "Rooks": (-58, -27, -15, -10, -5, -2, 9, 16, 30, 29, 32, 38, 46, 48, 58), \
                     "Queens": (
                         -39, -21, 3, 3, 14, 22, 28, 41, 43, 48, 56, 60, 60, 66, 67, 70, 71, 73, 79,
                         88,
                         88, 99, 102, 102, 106, 109, 113,
                         116)}  # 对应的棋子能走的格子数对应的分数，如King只能走0个格子的时候，得到-75分

    color_them = 0  # 初始化默认我方（AI）执白棋
    if color_AI == 0:  # 如果我方执黑棋
        color_them = 1
    KnightsMobilityBonus = 0
    KnightsMobility_us = getMobilityOfPieces(board, 2, color_AI)  ##我方马可以走的格子数
    for i in KnightsMobility_us:
        if (i != -1):
            KnightsMobilityBonus += MobilityBonus["Knights"][i]

    KnightsMobility_them = getMobilityOfPieces(board, 2, color_them)  ##对方马可以走的格子数
    for i in KnightsMobility_them:
        if (i != -1):
            KnightsMobilityBonus -= MobilityBonus["Knights"][i]

    BishopsMobilityBonus = 0
    BishopsMobility_us = getMobilityOfPieces(board, 3, color_AI)  ##我方象可以走的格子数
    for i in BishopsMobility_us:
        if (i != -1):
            BishopsMobilityBonus += MobilityBonus["Bishops"][i]
    BishopsMobility_them = getMobilityOfPieces(board, 3, color_them)  ##对方象可以走的格子数
    for i in BishopsMobility_them:
        if (i != -1):
            BishopsMobilityBonus -= MobilityBonus["Bishops"][i]

    RooksMobilityBonus = 0
    RooksMobility_us = getMobilityOfPieces(board, 4, color_AI)  ##我方车可以走得格子数
    for i in RooksMobility_us:
        if (i != -1):
            RooksMobilityBonus += MobilityBonus["Rooks"][i]
    RooksMobility_them = getMobilityOfPieces(board, 4, color_them)  ##对方车可以走得格子数
    for i in RooksMobility_them:
        if (i != -1):
            RooksMobilityBonus -= MobilityBonus["Rooks"][i]

    QueensMobilityBonus = 0
    QueensMobility_us = getMobilityOfPieces(board, 5, color_AI)  ##我方后可以走的格子数
    for i in QueensMobility_us:
        if (i != -1):
            QueensMobilityBonus += MobilityBonus["Queens"][i]
    QueensMobility_them = getMobilityOfPieces(board, 5, color_them)  ##对方后可以走的格子数
    for i in QueensMobility_them:
        if (i != -1):
            QueensMobilityBonus -= MobilityBonus["Queens"][i]

    MobilityValue = KnightsMobilityBonus + BishopsMobilityBonus + RooksMobilityBonus + QueensMobilityBonus
    return MobilityValue


def getMobilityOfPieces(board, piece_type, color):  # PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING 1-6
    pcs_mask = board.pieces_mask(piece_type, color)  # 返回棋子类型为piece_type的color方棋子的位棋盘
    pcs_position = chess.scan_forward(pcs_mask)
    attack_list = []
    for i in pcs_position:
        atks_mask = board.attacks_mask(i)
        atks_num = chess.popcount(atks_mask)
        overlap_mask = atks_mask & board.occupied_co[color]
        ol_num = chess.popcount(overlap_mask)
        attack_list.append(atks_num - ol_num)
    return attack_list
