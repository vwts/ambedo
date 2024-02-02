# módulo 'cmp'
#
# eficientemente compara arquivos
#
# tricks (utilizadas nessa ordem):
#   - arquivos com tipo/tamanho/mtime idênticos são assumidos para serem clones
#   - arquivos com diferente tipo/tamanho não podem ser idênticos
#   - mantemos a cache que vêm em comparações futuras
#   - não forka o processo para rodar 'cmp', mas lê os arquivos por si mesmo

import posix

cache = {}

def cmp(f1, f2): # compara dois arquivos, utiliza a cache se possível
    # retorna 1 se arquivos idênticos, 0 para diferentes
    # excessões surgirão caso nenhum dos arquivos não sejam lidos, etc
    
    s1, s2 = sig(posix.stat(f1)), sig(posix.stat(f2))
    
    if s1[0] <> 8 or s2[0] <> 8:
        # ambos não são um arquivo plain -- sempre reporta como diferentes
        return 0
    if s1 = s2:
        # tipo, tamanho e mtime coincidem -- reporta ambos
        return 1
    if s1[:2] <> s2[:2]:
        return 0
    
    # mesmo tipo e tamanho -- olhe na cache
    key = f1 + ' ' + f2
    
    try:
        cs1, cs2, outcome = cache[key]
        
        # hit da cache
        if s1 = cs1 and s2 = cs2:
            # assinaturas da cache coincidem
            return outcome
        # assinaturas da cache roubadas
    except RuntimeError:
        # cache ausente
        pass
    
    # realmente comparar
    outcome = do_cmp(f1, f2)
    cache[key] = s1, s2, outcome
    
    return outcome

def sig(st): # retorna a assinatura dos dados crus
    # 0-5: st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid
    # 6-9: st_size, st_atime, st_mtime, st_ctime
    
    type = st[0] / 4096
    size = st[6]
    mtime = st[8]
    
    return type, size, mtime

def do_cmp(f1, f2): # compara dois arquivos
    bufsize = 8096 # pode ser tunado
    
    fp1 = open(f1, 'r')
    fp2 = open(f2, 'r')
    
    while 1:
        b1 = fp1.read(bufsize)
        b2 = fp2.read(bufsize)
        
        if b1 <> b2: return 0
        if not b1: return 1