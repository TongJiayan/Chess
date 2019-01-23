

KEY = 0
VALUE = 1
FLAG = 2
DEPTH = 3
MOVE = 4

TABLE_NONE = 0
TABLE_EXACT = 1
TABLE_ALPHA = 2
TABLE_BETA = 3

size = 0
mask = 1
data = 2

def table_alloc(table, bits):
    table[size] = 1 << bits
    table[mask] = table[size] - 1
    # table.data = calloc(table.size, sizeof(Entry))
    table[data] = []
    length = table[size]
    for i in range(0, length):
        table[data].append([0, 0, 0, 0, ''])



def table_set(table, key, depth, value, flag):
    entry = TABLE_ENTRY(table, key)
    if entry[DEPTH] <= depth:
    	entry[KEY] = key
    	entry[DEPTH] = depth
    	entry[VALUE] = value
    	entry[FLAG] = flag



def table_get(table, key, depth, alpha, beta):
    entry = TABLE_ENTRY(table, key)
    if (entry[KEY] == key) and (entry[DEPTH] >= depth):
        if (entry[FLAG] == TABLE_EXACT):
            return True, entry[VALUE]
        elif((entry[FLAG] == TABLE_ALPHA) and (entry[VALUE] <= alpha)):
            return True, alpha
        elif((entry[FLAG] == TABLE_BETA) and (entry[VALUE] >= beta)):
        	return True, beta
    return False, 0


# move 在sort_move中的优化可能会使用到
# def table_get_move(table, key):
#     entry = TABLE_ENTRY(table, key)
#     if entry[KEY] == key
#         return 1, entry[MOVE]
#     return 0, NULL \..................................................................................


# def table_set_move(table, key, depth, move):
#     entry = TABLE_ENTRY(table, key)
#     if entry[DEPTH] <= depth:
#         entry[KEY] = key
#         entry[DEPTH] = depth
#         entry[FLAG] = TABLE_NONE
#         entry[MOVE] = move
#         # memcpy(&entry->move, move, sizeof(Move));

# ...






def TABLE_ENTRY(table, key):
	return table[data][(key & (table[mask]))]