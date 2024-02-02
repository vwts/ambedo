# módulo 'filewin'
#
# arquivo windows, uma sub-classe do textwin (que é uma sub-classe do gwin)

import stdwin
import textwin
import path

builtin_open = open

def readfile(fn): # retorna uma string contendo os conteúdos do arquivo
    fp = builtin_open(fn, 'r')
    
    a = ''
    n = 8096
    
    while 1:
        b = fp.read(n)
        
        if not b: break
        
        a = a + b
        
    return a

# arquivo window

def open_readonly(fn): # abre uma janela do arquivo
    w = textwin.open_readonly(fn, readfile(fn))
    w.fn = fn
    
    return w

def open(fn): # abre uma janela do arquivo
    w = textwin.open(fn, readfile(fn))
    w.fn = fn
    
    return w