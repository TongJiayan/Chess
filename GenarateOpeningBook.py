import chess.pgn
import chess.polyglot

file_amount = 1
file_read_count = 0
game_read_count = 0
step_count = 12
RESULT = '0'
WHO = 'WHITE'
RESULT_NUM = 0.0
DESTINY_DIRECTORY = 'C:/Users/Mi HD/Desktop/data/'
move_stastic_dict = {"0x463b96181691fc9c": {"e4": 1.0, "d4": 1.0}}
final_move_dict = {}


# 优化字典
def PolishDict():
    for (HashKey, Moves) in move_stastic_dict.items():
        final_move_dict[HashKey] = {
            findBestMove(Moves): move_stastic_dict[HashKey][findBestMove(Moves)]}


def findBestMove(mDict):
    maxValue = 0
    maxKey = 'e4'
    for (key, value) in mDict.items():
        if value >= maxValue:
            maxKey = key
            maxValue = value
    return maxKey


print('start')
while file_read_count != file_amount:
    file_read_count += 1
    print('read file amount:' + str(file_read_count))
    print('\n\n\n\n\n\n\n\n\n搞了一个文件:'+str(file_read_count))
    filename = str(file_read_count) + '.pgn'
    pgn = open(DESTINY_DIRECTORY + filename)
    game_reading = chess.pgn.read_game(pgn)
    while game_reading:
        node = game_reading
        game_read_count += 1
        print('read game amount:' + str(game_read_count))
        step_count = 0
        while node:
            if node.variations.__len__() == 0:
                break
            next_node = node.variations[0]
            board_hash = hex(chess.polyglot.zobrist_hash(node.board()))
            move = node.board().san(next_node.move)

            # print(node.board().san(next_node.move))
            if WHO == "WHITE":
                result_str = str(game_reading.headers["Result"])
                RESULT = result_str[0:result_str.index('-')]
            else:
                result_str = str(game_reading.headers["Result"])
                RESULT = result_str[result_str.index('-') + 1:]

            if RESULT == "1":
                RESULT_NUM = 1
            elif RESULT == "0":
                RESULT_NUM = 0
            elif RESULT == "1/2":
                RESULT_NUM = 0.5

            if board_hash in move_stastic_dict:
                if move in move_stastic_dict[board_hash]:
                    move_stastic_dict[board_hash][move] += RESULT_NUM
                elif RESULT_NUM != 0:
                    move_stastic_dict[board_hash][move] = RESULT_NUM
            else:
                move_stastic_dict[board_hash] = {move: RESULT_NUM}
            step_count += 1
            if (step_count == 15):
                break
            node = next_node

        game_reading = chess.pgn.read_game(pgn)

PolishDict()
file_output = open(DESTINY_DIRECTORY + 'open_dict.txt', 'w', encoding="utf-8")
file_output.write(str(final_move_dict))
file_output.close()
print('end')
