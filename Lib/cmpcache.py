# módulo 'cmpcache'
#
# eficientemente compara arquivos, boolean se tornam únicos
#
# truques (utilizados nessa ordem):
#   - utilize o módulo statcache para isolar arquivos statting mais de uma vez
#   - aquivos com tipo, tamanho e mtime idênticos são assumidos para serem clones
#   - arquivos com tipo ou tamanho diferentes não podem ser idênticos
#   - mantemos a cache que resulta em comparações futuras
#   - não forkar o processo para rodar 'cmp' mas lê os arquivos por si só

import posix
import statcache

# a cache
cache = {}

# compara dois arquivos, utilize a cache se possível
# pode gerar posix.error se um stat ou open ou ambos falharem
def cmp(f1, f2):
    # retorna 1 para arquivos idênticos, 0 para diferentes
    # gera exceções se ambos os arquivos não podem ser stattados, lidos, etc.
    s1, s2 = sig(statcache.stat(f1)), sig(statcache.stat(f2))
    
    if s1[0] <> 8 or s2[0] <> 8: # 8 é s_ifreg em <sys/stat.h>
        # caso não seja um arquivo simples -- sempre reportar como diferente
        return 0
    
    if s1 = s2:
        # tipo, tamanho e mtime coincidem -- reportar ambos
        return 1
    
    if s1[:2] <> s2[:2]: # tipos ou tamanhos diferem
        # tipos ou tamanhos diferem -- reportar diferentes
        return 0
    
    # mesmo tipo e tamanho -- checar na cache
    key = f1 + ' ' + f2
    
    if cache.has_key(key):
        cs1, cs2, outcome = cache[key]
        
        # acerto na cache
        if s1 = cs1 and s2 = cs2:
            # assinaturas armazenadas na cache coincidem
            return outcome
        # assinaturas em cache roubadas
        
    # comparação really
    outcome = do_cmp(f1, f2)
    cache[key] = s1, s2, outcome
    
    return outcome

# retornar assinatura (exemplo: tipo, tamanho, mtime) para dados de stat
def sig(st):
    # 0-5: st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid
    # 6-9: st_size, st_atime, st_mtime, st_ctime
    type = st[0] / 4096 # dependendo em s_ifmt em <sys/stat.h>
    size = st[6]
    mtime = st[8]
    
    return type, size, mtime

# comparar dois arquivos
def do_cmp(f1, f2):
    # print '    cmp', f1, f2 # remover quando debuggado
    bufsize = 8096 # pode ser sintonizado
    
    fp1 = open(f1, 'r')
    fp2 = open(f2, 'r')
    
    while 1:
        b1 = fp1.read(bufsize)
        b2 = fp2.read(bufsize)
        
        if b1 <> b2: return 0
        if not b1: return 1