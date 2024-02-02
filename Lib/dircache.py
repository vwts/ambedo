# módulo 'dircache'
#
# retorna uma lista sorteada dos arquivos em um diretório posix, utilizando
# a cache para isolar o diretório mais do que o necessário
# também contém uma sub-rotina para slashes no diretório

import posix
import path

cache = {}

def listdir(path): # lista conteúdos do diretório, utilizando cache
    try:
        cached_mtime, list = cache[path]
        
        del cache[path]
    except RuntimeError:
        cached_mtime, list = -1, []
    try:
        mtime = posix.stat(path)[8]
    except posix.error:
        return []
    if mtime <> cached_mtime:
        try:
            list = posix.listdir(path)
        except posix.error:
            return []
        list.sort()
        
    cache[path] = mtime, list
    
    return list

opendir = listdir

def annotate(head, list): # adicionar sufixos '/' para os diretórios
    for i in range(len(list)):
        if path.isdir(path.cat(head, list[i])):
            list[i] = list[i] + '/'