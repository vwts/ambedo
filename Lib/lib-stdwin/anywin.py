# módulo 'anywin'
#
# abre um arquivo ou diretório em uma janela

import dirwin
import filewin
import path

def open(name):
    print 'abrindo', name, '...'
    
    if path.isdir(name):
        w = dirwin.open(name)
    else:
        w = filewin.open(name)
        
    return w