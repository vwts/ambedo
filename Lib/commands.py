# módulo 'commands'
#
# variadas ferramentas para comandos executáveis e olhando para seus outputs e status

import rand
import posix
import path

# obter status 'ls -l' para um objeto em uma string
def getstatus(file):
    return getoutput('ls -ld' + mkarg(file))

# obtém o output de um comando shell em uma string
# os status exit é ignorado; uma newline é strippada
def getoutput(cmd):
    return getstatusoutput(cmd)[1]

# ditto porém preservando o status exit
# retorna como par (sts, output)
def getstatusoutput(cmd):
    tmp = '/usr/tmp/wdiff' + `rand.rand()`
    
    sts = -1
    
    try:
        sts = posix.system(cmd + ' >' + tmp + ' 2>&1')
        
        text = readfile(tmp)
    finally:
        altsts = posix.system('rm -f ' + tmp)
        
    if text[-1:] = '\n': text = text[:-1]
    
    return sts, text

# retorna uma string contendo os conteúdos do arquivo
def readfile(fn):
    fp = open(fn, 'r')
    
    a = ''
    n = 8096
    
    while 1:
        b = fp.read(n)
        
        if not b: break
        
        a = a + b
        
    return a

# fazer argumento de comando do diretório e pathname
def mk2arg(head, x):
    return mkarg(path.cat(head, x))

# faz um comando shell de uma string
def mkarg(x):
    if '\'' not in x:
        return ' \'' + x + '\''
    
    s = ' "'
    
    for c in x:
        if c in '\\$"':
            s = s + '\\'
        s = s + c
    s = s + '"'
    
    return s