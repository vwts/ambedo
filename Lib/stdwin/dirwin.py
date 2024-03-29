# módulo 'dirwin'
#
# janelas do diretório, uma sub-classe do listwin

import gwin
import listwin
import anywin
import path
import dircache

def action(w, string, i, detail):
    (h, v), clicks, button, mask = detail
    
    if clicks = 2:
        name = path.cat(w.name, string)
        
        try:
            w = anywin.open(name)
        except posix.error, why:
            stdwin.message('não pode abrir ' + name + ': ' + why[1])
            
def open(name):
    name = path.cat(name, '')
    
    list = dircache.opendir(name)[:]
    list.sort()
    
    dircache.annotate(name, list)
    
    w = listwin.open(name, list)
    w.name = name
    w.action = action
    
    return w