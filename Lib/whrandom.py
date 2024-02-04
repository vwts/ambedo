# gerador de número wichmann-hill aleatório
#
# wichmann, b. a. & hill, i. d. (1982)
# algoritmo as 183:
# um eficiente e portável gerador de número pseudo-aleatório
# estatísticas 31 aplicadas (1982) 188-190
#
# veja também:
#     correção para o algoritmo as 183
#     estatísticas 33 aplicadas (1984) 123
#
#     mcleod, a. i. (1985)
#     um remark do algoritmo as 183
#     estatísticas 34 aplicadas (1985), 198-200
#
# uso:
# whrandom.random()
#
# whrandom.seed()
#
# traduzido por guido van rossum da fonte c fornecida por adrian baddeley

# a semente
_seed = [0, 0, 0]

# setar a semente
def seed(x, y, z):
    _seed[:] = [x, y, z]
    
# retornar o próximo número aleatório no alcance [0.0 .. 1.0]
def random():
    from math import floor # função floor()
    
    #
    
    [x, y, z] = _seed
    
    x = 171 * (x % 177) - 2 * (x / 177)
    y = 172 * (y % 176) - 35 * (y / 176)
    z = 170 * (z % 178) - 63 * (z / 178)
    
    #
    
    if x < 0: x = x + 30269
    if y < 0: y = y + 30307
    if z < 0: z = z + 30323
    
    #
    
    _seed[:] = [x, y, z]
    
    #
    
    term = float(x) / 30269.0 + float(y) / 30307.0 + float(z) / 30323.0
    rand = term - floor(term)
    
    #
    
    if rand >= 1.0: rand = 0.0
    
    #
    
    return rand

# inicializar a partir do tempo atual
def init():
    import time
    
    t = time.time()
    
    seed(t % 256, t / 256 % 256, t / 65536 % 256)
    
# certificar-se que o gerador é um preset ao valor não-zero
init()