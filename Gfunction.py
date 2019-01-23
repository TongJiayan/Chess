
def PIECE(x):
	return ((x) & 0x0f)
def COLOR(x):
	return ((x) & 0x10)


def BIT(sq):
	return 1 << (sq)

def RF(rank, file) :
	return ((rank) * 8 + (file))




# m_w = 0x8eeee9fb
# m_z = 0x433072e9




# def prng():
# 	m_z = 36969 * (m_z & 65535) + (m_z >> 16)
#     m_w = 18000 * (m_w & 65535) + (m_w >> 16)
#     return (m_z << 16) + m_w

# .s....................................................................................................
# void prng_seed(unsigned int seed) {
#     m_w = seed;
#     m_z = seed;
# }
