import Gfunction
import chess
# import bb
import chess
import chess.polyglot

WHITE = 0x00
BLACK = 0x10

EMPTY = 0x00
PAWN = 0x01
KNIGHT = 0x02
BISHOP = 0x03
ROOK = 0x04
QUEEN = 0x05
KING = 0x06

WHITE_PAWN = 0x01
WHITE_KNIGHT = 0x02
WHITE_BISHOP = 0x03
WHITE_ROOK = 0x04
WHITE_QUEEN = 0x05
WHITE_KING = 0x06

BLACK_PAWN = 0x11
BLACK_KNIGHT = 0x12
BLACK_BISHOP = 0x13
BLACK_ROOK = 0x14
BLACK_QUEEN = 0x15
BLACK_KING = 0x16



CASTLE_ALL = 15
CASTLE_WHITE = 3
CASTLE_BLACK = 12
CASTLE_WHITE_KING = 1
CASTLE_WHITE_QUEEN = 2
CASTLE_BLACK_KING = 4
CASTLE_BLACK_QUEEN = 8

MATERIAL_PAWN = 100
MATERIAL_KNIGHT = 320
MATERIAL_BISHOP = 330
MATERIAL_ROOK = 500
MATERIAL_QUEEN = 900
MATERIAL_KING = 20000


# board_info
# 使用dict

#开局时候对棋盘的各种信息进行初始化
def board_start(board, board_info):
	# board_clear()
	# board_info.....=0
    # int color
    # int castle
    board_info['black_queens'] = 0
    board_info['black_rooks'] = 0
    board_info['white_material'] = 0
    board_info['black_material'] = 0
    board_info['white_position'] = 0
    board_info['black_position'] = 0
    board_info['hash'] = chess.polyglot.zobrist_hash(board)
    board_info['color_AI']=1 #初始化AI执白棋
    board_info['null_move_pace']=0
    # bb ep;
    # board_info.all;
    # bb white;
    # bb black;
    # board_info['white_pawns'] = 0
    # bb black_pawns;
    # bb white_knights;
    # bb black_knights;
    # bb white_bishops;
    # bb black_bishops;
    # bb white_rooks;
    # bb black_rooks;
    # bb white_queens;
    # bb black_queens;
    # bb white_kings;
    # bb black_kings;
    # board_info.hash;
    # bb pawn_hash;

    for file in range(0, 8):
        board_initial(board, Gfunction.RF(1, file), WHITE_PAWN, board_info)
        board_initial(board, Gfunction.RF(6, file), BLACK_PAWN, board_info)

    board_initial(board, Gfunction.RF(0, 0), WHITE_ROOK, board_info)
    board_initial(board, Gfunction.RF(0, 1), WHITE_KNIGHT, board_info)
    board_initial(board, Gfunction.RF(0, 2), WHITE_BISHOP, board_info)
    board_initial(board, Gfunction.RF(0, 3), WHITE_QUEEN, board_info)
    board_initial(board, Gfunction.RF(0, 4), WHITE_KING, board_info)
    board_initial(board, Gfunction.RF(0, 5), WHITE_BISHOP, board_info)
    board_initial(board, Gfunction.RF(0, 6), WHITE_KNIGHT, board_info)
    board_initial(board, Gfunction.RF(0, 7), WHITE_ROOK, board_info)
    board_initial(board, Gfunction.RF(7, 0), BLACK_ROOK, board_info)
    board_initial(board, Gfunction.RF(7, 1), BLACK_KNIGHT, board_info)
    board_initial(board, Gfunction.RF(7, 2), BLACK_BISHOP, board_info)
    board_initial(board, Gfunction.RF(7, 3), BLACK_QUEEN, board_info)
    board_initial(board, Gfunction.RF(7, 4), BLACK_KING, board_info)
    board_initial(board, Gfunction.RF(7, 5), BLACK_BISHOP, board_info)
    board_initial(board, Gfunction.RF(7, 6), BLACK_KNIGHT, board_info)
    board_initial(board, Gfunction.RF(7, 7), BLACK_ROOK, board_info)
	



def board_initial(board, sq, piece, board_info):
    if Gfunction.COLOR(piece) == 0x10:
        piece_type = Gfunction.PIECE(piece)
        if piece_type == PAWN:
            board_info['black_material'] += MATERIAL_PAWN
            board_info['black_position'] += POSITION_BLACK_PAWN[sq]
        elif piece_type == KNIGHT:
            board_info['black_material'] += MATERIAL_KNIGHT
            board_info['black_position'] += POSITION_BLACK_KNIGHT[sq]
        elif piece_type == BISHOP:
            board_info['black_material'] += MATERIAL_BISHOP
            board_info['black_position'] += POSITION_BLACK_BISHOP[sq]
        elif piece_type == ROOK:
            board_info['black_material'] += MATERIAL_ROOK
            board_info['black_position'] += POSITION_BLACK_ROOK[sq]
        elif piece_type == QUEEN:
            board_info['black_material'] += MATERIAL_QUEEN
            board_info['black_position'] += POSITION_BLACK_QUEEN[sq]
        elif piece_type == KING:
            board_info['black_material'] += MATERIAL_KING
            board_info['black_position'] += POSITION_BLACK_KING[sq]
    else:
        piece_type = Gfunction.PIECE(piece)
        if piece_type == PAWN:
            board_info['white_material'] += MATERIAL_PAWN
            board_info['white_position'] += POSITION_WHITE_PAWN[sq]
        elif piece_type == KNIGHT:
            board_info['white_material'] += MATERIAL_KNIGHT
            board_info['white_position'] += POSITION_WHITE_KNIGHT[sq]
        elif piece_type == BISHOP:
            board_info['white_material'] += MATERIAL_BISHOP
            board_info['white_position'] += POSITION_WHITE_BISHOP[sq]
        elif piece_type == ROOK:
            board_info['white_material'] += MATERIAL_ROOK
            board_info['white_position'] += POSITION_WHITE_ROOK[sq]
        elif piece_type == QUEEN:
            board_info['white_material'] += MATERIAL_QUEEN
            board_info['white_position'] += POSITION_WHITE_QUEEN[sq]
        elif piece_type == KING:
            board_info['white_material'] += MATERIAL_KING
            board_info['white_position'] += POSITION_WHITE_KING[sq]


# 出入下一步要走的san,设置棋盘信息
def board_info_set(board, san, board_info):
    move = board.parse_san(san).uci()
    src = move[0:2].upper()
    dst = move[2:4].upper()
    str_src = 'chess.' + src
    str_dst = 'chess.' + dst
    # 求出起点和终点在64个格子中的位置
    square_src = eval(str_src)
    square_dst = eval(str_dst)


    color_src = bool(board.occupied_co[chess.WHITE] & chess.BB_SQUARES[square_src])
    #white=1,black=0

    # 删除src
    if not color_src: #if color_src==BLACK
        # src == black
        piece_type = board.piece_type_at(square_src)

        if piece_type == PAWN:
            board_info['black_material'] -= MATERIAL_PAWN
            board_info['black_position'] -= POSITION_BLACK_PAWN[square_src]
        elif piece_type == KNIGHT:
               board_info['black_material'] -= MATERIAL_KNIGHT
               board_info['black_position'] -= POSITION_BLACK_KNIGHT[square_src]
        elif piece_type == BISHOP:
               board_info['black_material'] -= MATERIAL_BISHOP
               board_info['black_position'] -= POSITION_BLACK_BISHOP[square_src]
        elif piece_type == ROOK:
               board_info['black_material'] -= MATERIAL_ROOK
               board_info['black_position'] -= POSITION_BLACK_ROOK[square_src]
        elif piece_type == QUEEN:
               board_info['black_material'] -= MATERIAL_QUEEN
               board_info['black_position'] -= POSITION_BLACK_QUEEN[square_src]
        elif piece_type == KING:
               board_info['black_material'] -= MATERIAL_KING
               board_info['black_position'] -= POSITION_BLACK_KING[square_src]
    else:
        # src == white
        piece_type = board.piece_type_at(square_src)

        if piece_type == PAWN:
            board_info['white_material'] -= MATERIAL_PAWN
            board_info['white_position'] -= POSITION_WHITE_PAWN[square_src]
        elif piece_type == KNIGHT:
            board_info['white_material'] -= MATERIAL_KNIGHT
            board_info['white_position'] -= POSITION_WHITE_KNIGHT[square_src]
        elif piece_type == BISHOP:
            board_info['white_material'] -= MATERIAL_BISHOP
            board_info['white_position'] -= POSITION_WHITE_BISHOP[square_src]
        elif piece_type == ROOK:
            board_info['white_material'] -= MATERIAL_ROOK
            board_info['white_position'] -= POSITION_WHITE_ROOK[square_src]
        elif piece_type == QUEEN:
            board_info['white_material'] -= MATERIAL_QUEEN
            board_info['white_position'] -= POSITION_WHITE_QUEEN[square_src]
        elif piece_type == KING:
            board_info['white_material'] -= MATERIAL_KING
            board_info['white_position'] -= POSITION_WHITE_KING[square_src]


    # dst处不为空 -- 出现吃子的现象 删除dst原来位置内容
    if bool(board.occupied & chess.BB_SQUARES[square_dst]):
        color_dst = bool(board.occupied_co[chess.WHITE] & chess.BB_SQUARES[square_dst])
        if not color_dst:
            # dst == black
            piece_type = board.piece_type_at(square_dst)

            if piece_type == PAWN:
                board_info['black_material'] -= MATERIAL_PAWN
                board_info['black_position'] -= POSITION_BLACK_PAWN[square_dst]
            elif piece_type == KNIGHT:
                   board_info['black_material'] -= MATERIAL_KNIGHT
                   board_info['black_position'] -= POSITION_BLACK_KNIGHT[square_dst]
            elif piece_type == BISHOP:
                   board_info['black_material'] -= MATERIAL_BISHOP
                   board_info['black_position'] -= POSITION_BLACK_BISHOP[square_dst]
            elif piece_type == ROOK:
                   board_info['black_material'] -= MATERIAL_ROOK
                   board_info['black_position'] -= POSITION_BLACK_ROOK[square_dst]
            elif piece_type == QUEEN:
                   board_info['black_material'] -= MATERIAL_QUEEN
                   board_info['black_position'] -= POSITION_BLACK_QUEEN[square_dst]
            elif piece_type == KING:
                   board_info['black_material'] -= MATERIAL_KING
                   board_info['black_position'] -= POSITION_BLACK_KING[square_dst]
        else:
            # dst == white
            piece_type = board.piece_type_at(square_dst)

            if piece_type == PAWN:
                board_info['white_material'] -= MATERIAL_PAWN
                board_info['white_position'] -= POSITION_WHITE_PAWN[square_dst]
            elif piece_type == KNIGHT:
                board_info['white_material'] -= MATERIAL_KNIGHT
                board_info['white_position'] -= POSITION_WHITE_KNIGHT[square_dst]
            elif piece_type == BISHOP:
                board_info['white_material'] -= MATERIAL_BISHOP
                board_info['white_position'] -= POSITION_WHITE_BISHOP[square_dst]
            elif piece_type == ROOK:
                board_info['white_material'] -= MATERIAL_ROOK
                board_info['white_position'] -= POSITION_WHITE_ROOK[square_dst]
            elif piece_type == QUEEN:
                board_info['white_material'] -= MATERIAL_QUEEN
                board_info['white_position'] -= POSITION_WHITE_QUEEN[square_dst]
            elif piece_type == KING:
                board_info['white_material'] -= MATERIAL_KING
                board_info['white_position'] -= POSITION_WHITE_KING[square_dst]



    # 对dst位置进行添加  ...考虑晋升
    promotion = 'q'
    is_promotion = bool(len(move) == 5)

    if not color_src:
        # src == black
        if not is_promotion:
            piece_type = board.piece_type_at(square_src)
        else:
            promotion = move[4]
            piece_type = chess.PIECE_SYMBOLS.index(promotion)

        if piece_type == PAWN:
            board_info['black_material'] += MATERIAL_PAWN
            board_info['black_position'] += POSITION_BLACK_PAWN[square_dst]
        elif piece_type == KNIGHT:
            board_info['black_material'] += MATERIAL_KNIGHT
            board_info['black_position'] += POSITION_BLACK_KNIGHT[square_dst]
        elif piece_type == BISHOP:
            board_info['black_material'] += MATERIAL_BISHOP
            board_info['black_position'] += POSITION_BLACK_BISHOP[square_dst]
        elif piece_type == ROOK:
            board_info['black_material'] += MATERIAL_ROOK
            board_info['black_position'] += POSITION_BLACK_ROOK[square_dst]
        elif piece_type == QUEEN:
            board_info['black_material'] += MATERIAL_QUEEN
            board_info['black_position'] += POSITION_BLACK_QUEEN[square_dst]
        elif piece_type == KING:
            board_info['black_material'] += MATERIAL_KING
            board_info['black_position'] += POSITION_BLACK_KING[square_dst]
    else:
        # src == white
        if not is_promotion:
            piece_type = board.piece_type_at(square_src)
        else:
            promotion = move[4]
            piece_type = chess.PIECE_SYMBOLS.index(promotion)

        if piece_type == PAWN:
            board_info['white_material'] += MATERIAL_PAWN
            board_info['white_position'] += POSITION_WHITE_PAWN[square_dst]
        elif piece_type == KNIGHT:
            board_info['white_material'] += MATERIAL_KNIGHT
            board_info['white_position'] += POSITION_WHITE_KNIGHT[square_dst]
        elif piece_type == BISHOP:
            board_info['white_material'] += MATERIAL_BISHOP
            board_info['white_position'] += POSITION_WHITE_BISHOP[square_dst]
        elif piece_type == ROOK:
            board_info['white_material'] += MATERIAL_ROOK
            board_info['white_position'] += POSITION_WHITE_ROOK[square_dst]
        elif piece_type == QUEEN:
            board_info['white_material'] += MATERIAL_QUEEN
            board_info['white_position'] += POSITION_WHITE_QUEEN[square_dst]
        elif piece_type == KING:
            board_info['white_material'] += MATERIAL_KING;
            board_info['white_position'] += POSITION_WHITE_KING[square_dst]
        



def score_san(board, san):#返回board情形下，进行san走子获得的分数
    result = 0
    piece_material_src = 0
    piece_material_dst = 0
    capture_material = 0
    move = board.parse_san(san).uci()
    src = move[0:2].upper()
    dst = move[2:4].upper()
    str_src = 'chess.' + src
    str_dst = 'chess.' + dst
    # 求出起点和终点在64个格子中的位置
    square_src = eval(str_src)
    square_dst = eval(str_dst)


    color_src = bool(board.occupied_co[chess.WHITE] & chess.BB_SQUARES[square_src])
    # 删除src
    if not color_src:
        # src == black
        piece_type = board.piece_type_at(square_src)

        if piece_type == PAWN:
            piece_material_src = MATERIAL_PAWN
            result -= POSITION_BLACK_PAWN[square_src]
        elif piece_type == KNIGHT:
            piece_material_src = MATERIAL_KNIGHT
            result -= POSITION_BLACK_KNIGHT[square_src]
        elif piece_type == BISHOP:
            piece_material_src = MATERIAL_BISHOP
            result -= POSITION_BLACK_BISHOP[square_src]
        elif piece_type == ROOK:
            piece_material_src = MATERIAL_ROOK
            result -= POSITION_BLACK_ROOK[square_src]
        elif piece_type == QUEEN:
            piece_material_src = MATERIAL_QUEEN
            result -= POSITION_BLACK_QUEEN[square_src]
        elif piece_type == KING:
            piece_material_src = MATERIAL_KING
            result -= POSITION_BLACK_KING[square_src]
    else:
        # src == white
        piece_type = board.piece_type_at(square_src)

        if piece_type == PAWN:
            piece_material_src = MATERIAL_PAWN
            result -= POSITION_WHITE_PAWN[square_src]
        elif piece_type == KNIGHT:
            piece_material_src = MATERIAL_KNIGHT
            result -= POSITION_WHITE_KNIGHT[square_src]
        elif piece_type == BISHOP:
            piece_material_src = MATERIAL_BISHOP
            result -= POSITION_WHITE_BISHOP[square_src]
        elif piece_type == ROOK:
            piece_material_src = MATERIAL_ROOK
            result -= POSITION_WHITE_ROOK[square_src]
        elif piece_type == QUEEN:
            piece_material_src = MATERIAL_QUEEN
            result -= POSITION_WHITE_QUEEN[square_src]
        elif piece_type == KING:
            piece_material_src = MATERIAL_KING;
            result -= POSITION_WHITE_KING[square_src]


    # dst处不为空 -- 出现吃子的现象 删除dst原来位置内容
    if bool(board.occupied & chess.BB_SQUARES[square_dst]):
        color_dst = bool(board.occupied_co[chess.WHITE] & chess.BB_SQUARES[square_dst])
        if not color_dst:
            # dst == black
            piece_type = board.piece_type_at(square_dst)

            if piece_type == PAWN:
                capture_material = MATERIAL_PAWN
            elif piece_type == KNIGHT:
                capture_material = MATERIAL_KNIGHT
            elif piece_type == BISHOP:
                capture_material = MATERIAL_BISHOP
            elif piece_type == ROOK:
                capture_material = MATERIAL_ROOK
            elif piece_type == QUEEN:
                capture_material = MATERIAL_QUEEN
            elif piece_type == KING:
                capture_material = MATERIAL_KING
        else:
            # dst == white
            piece_type = board.piece_type_at(square_dst)

            if piece_type == PAWN:
                capture_material = MATERIAL_PAWN
            elif piece_type == KNIGHT:
                capture_material = MATERIAL_KNIGHT
            elif piece_type == BISHOP:
                capture_material = MATERIAL_BISHOP
            elif piece_type == ROOK:
                capture_material = MATERIAL_ROOK
            elif piece_type == QUEEN:
                capture_material = MATERIAL_QUEEN
            elif piece_type == KING:
                capture_material = MATERIAL_KING



    # 对dst位置进行添加  ...考虑晋升
    promotion = 'q'
    is_promotion = bool(len(move) == 5)

    if not color_src:
        # src == black
        if not is_promotion:
            piece_type = board.piece_type_at(square_src)
        else:
            promotion = move[4]
            piece_type = chess.PIECE_SYMBOLS.index(promotion)

        if piece_type == PAWN:
            piece_material_dst = MATERIAL_PAWN
            result += POSITION_BLACK_PAWN[square_dst]
        elif piece_type == KNIGHT:
            piece_material_dst = MATERIAL_KNIGHT
            result += POSITION_BLACK_KNIGHT[square_dst]
        elif piece_type == BISHOP:
            piece_material_dst = MATERIAL_BISHOP
            result += POSITION_BLACK_BISHOP[square_dst]
        elif piece_type == ROOK:
            piece_material_dst = MATERIAL_ROOK
            result += POSITION_BLACK_ROOK[square_dst]
        elif piece_type == QUEEN:
            piece_material_dst = MATERIAL_QUEEN
            result += POSITION_BLACK_QUEEN[square_dst]
        elif piece_type == KING:
            piece_material_dst = MATERIAL_KING
            result += POSITION_BLACK_KING[square_dst]
    else:
        # src == white
        if not is_promotion:
            piece_type = board.piece_type_at(square_src)
        else:
            promotion = move[4]
            piece_type = chess.PIECE_SYMBOLS.index(promotion)

        if piece_type == PAWN:
            piece_material_dst = MATERIAL_PAWN
            result += POSITION_WHITE_PAWN[square_dst]
        elif piece_type == KNIGHT:
            piece_material_dst = MATERIAL_KNIGHT
            result += POSITION_WHITE_KNIGHT[square_dst]
        elif piece_type == BISHOP:
            piece_material_dst = MATERIAL_BISHOP
            result += POSITION_WHITE_BISHOP[square_dst]
        elif piece_type == ROOK:
            piece_material_dst = MATERIAL_ROOK
            result += POSITION_WHITE_ROOK[square_dst]
        elif piece_type == QUEEN:
            piece_material_dst = MATERIAL_QUEEN
            result += POSITION_WHITE_QUEEN[square_dst]
        elif piece_type == KING:
            piece_material_dst = MATERIAL_KING;
            result += POSITION_WHITE_KING[square_dst]

    result = result + capture_material + piece_material_dst - piece_material_src
    return result






POSITION_WHITE_PAWN = [\
      0,  0,  0,  0,  0,  0,  0,  0,\
      5, 10, 10,-20,-20, 10, 10,  5,\
      5, -5,-10,  0,  0,-10, -5,  5,\
      0,  0,  0, 20, 20,  0,  0,  0,\
      5,  5, 10, 25, 25, 10,  5,  5,\
     10, 10, 20, 30, 30, 20, 10, 10,\
     50, 50, 50, 50, 50, 50, 50, 50,\
      0,  0,  0,  0,  0,  0,  0,  0]

POSITION_WHITE_KNIGHT = [\
    -50,-40,-30,-30,-30,-30,-40,-50,\
    -40,-20,  0,  5,  5,  0,-20,-40,\
    -30,  5, 10, 15, 15, 10,  5,-30,\
    -30,  0, 15, 20, 20, 15,  0,-30,\
    -30,  5, 15, 20, 20, 15,  5,-30,\
    -30,  0, 10, 15, 15, 10,  0,-30,\
    -40,-20,  0,  0,  0,  0,-20,-40,\
    -50,-40,-30,-30,-30,-30,-40,-50]

POSITION_WHITE_BISHOP = [\
    -20,-10,-10,-10,-10,-10,-10,-20,\
    -10,  5,  0,  0,  0,  0,  5,-10,\
    -10, 10, 10, 10, 10, 10, 10,-10,\
    -10,  0, 10, 10, 10, 10,  0,-10,\
    -10,  5,  5, 10, 10,  5,  5,-10,\
    -10,  0,  5, 10, 10,  5,  0,-10,\
    -10,  0,  0,  0,  0,  0,  0,-10,\
    -20,-10,-10,-10,-10,-10,-10,-20]

POSITION_WHITE_ROOK = [\
      0,  0,  0,  5,  5,  0,  0,  0,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
      5, 10, 10, 10, 10, 10, 10,  5,\
      0,  0,  0,  0,  0,  0,  0,  0]

POSITION_WHITE_QUEEN = [\
    -20,-10,-10, -5, -5,-10,-10,-20,\
    -10,  0,  5,  0,  0,  0,  0,-10,\
    -10,  5,  5,  5,  5,  5,  0,-10,\
      0,  0,  5,  5,  5,  5,  0, -5,\
     -5,  0,  5,  5,  5,  5,  0, -5,\
    -10,  0,  5,  5,  5,  5,  0,-10,\
    -10,  0,  0,  0,  0,  0,  0,-10,\
    -20,-10,-10, -5, -5,-10,-10,-20]

POSITION_WHITE_KING = [\
     20, 30, 10,  0,  0, 10, 30, 20,\
     20, 20,  0,  0,  0,  0, 20, 20,\
    -10,-20,-20,-20,-20,-20,-20,-10,\
    -20,-30,-30,-40,-40,-30,-30,-20,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30]

POSITION_BLACK_PAWN = [\
      0,  0,  0,  0,  0,  0,  0,  0,\
     50, 50, 50, 50, 50, 50, 50, 50,\
     10, 10, 20, 30, 30, 20, 10, 10,\
      5,  5, 10, 25, 25, 10,  5,  5,\
      0,  0,  0, 20, 20,  0,  0,  0,\
      5, -5,-10,  0,  0,-10, -5,  5,\
      5, 10, 10,-20,-20, 10, 10,  5,\
      0,  0,  0,  0,  0,  0,  0,  0]

POSITION_BLACK_KNIGHT = [\
    -50,-40,-30,-30,-30,-30,-40,-50,\
    -40,-20,  0,  0,  0,  0,-20,-40,\
    -30,  0, 10, 15, 15, 10,  0,-30,\
    -30,  5, 15, 20, 20, 15,  5,-30,\
    -30,  0, 15, 20, 20, 15,  0,-30,\
    -30,  5, 10, 15, 15, 10,  5,-30,\
    -40,-20,  0,  5,  5,  0,-20,-40,\
    -50,-40,-30,-30,-30,-30,-40,-50]

POSITION_BLACK_BISHOP = [\
    -20,-10,-10,-10,-10,-10,-10,-20,\
    -10,  0,  0,  0,  0,  0,  0,-10,\
    -10,  0,  5, 10, 10,  5,  0,-10,\
    -10,  5,  5, 10, 10,  5,  5,-10,\
    -10,  0, 10, 10, 10, 10,  0,-10,\
    -10, 10, 10, 10, 10, 10, 10,-10,\
    -10,  5,  0,  0,  0,  0,  5,-10,\
    -20,-10,-10,-10,-10,-10,-10,-20]

POSITION_BLACK_ROOK = [\
      0,  0,  0,  0,  0,  0,  0,  0,\
      5, 10, 10, 10, 10, 10, 10,  5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
     -5,  0,  0,  0,  0,  0,  0, -5,\
      0,  0,  0,  5,  5,  0,  0,  0]

POSITION_BLACK_QUEEN = [\
    -20,-10,-10, -5, -5,-10,-10,-20,\
    -10,  0,  0,  0,  0,  0,  0,-10,\
    -10,  0,  5,  5,  5,  5,  0,-10,\
     -5,  0,  5,  5,  5,  5,  0, -5,\
      0,  0,  5,  5,  5,  5,  0, -5,\
    -10,  5,  5,  5,  5,  5,  0,-10,\
    -10,  0,  5,  0,  0,  0,  0,-10,\
    -20,-10,-10, -5, -5,-10,-10,-20]

POSITION_BLACK_KING = [\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -30,-40,-40,-50,-50,-40,-40,-30,\
    -20,-30,-30,-40,-40,-30,-30,-20,\
    -10,-20,-20,-20,-20,-20,-20,-10,\
     20, 20,  0,  0,  0,  0, 20, 20,\
     20, 30, 10,  0,  0, 10, 30, 20]
