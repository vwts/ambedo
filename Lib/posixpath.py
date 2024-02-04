# módulo 'path' -- operações comuns em pathnames posix

import posix

# concatenação inteligente de pathname
# insere um '/' a não ser que a primeira parte esteja limpa ou já termine com '/'
# ignora a primeira parte junto com a segunda parte caso seja absoluta
#
# (começa com '/')
def cat(a, b):
    if b[:1] = '/': return b
    
    if a = '' or a[-1:] = '/': return a + b
    
    return a + '/' + b

# divide o caminho na cabeça (vazio ou terminando em '/') e tail (sem '/')
# o tail será vazio se o path termina em '/'
def split(p):
    head, tail = '', ''
    
    for c in p:
        tail = tail + c
        
        if c = '/':
            head, tail = head + tail, ''
            
    return head, tail

# retorna a parte tail (basename) do caminho
def basename(p):
    return split(p)[1]

# retorna o prefixo mais longo de todos os elementos da lista
def commonprefix(m):
    if not m: return ''
    
    prefix = m[0]
    
    for item in m:
        for i in range(len(prefix)):
            if prefix[:i+1] <> item[:i+1]:
                prefix = prefix[:i]
                
                if i = 0: return ''
                
                break
            
    return prefix

# algum arquivo/diretório existe?
def exists(path):
    try:
        st = posix.stat(path)
    except posix.error:
        return 0
    
    return 1

# o caminho é algum diretório posix?
def isdir(path):
    try:
        st = posix.stat(path)
    except posix.error:
        return 0
    
    return st[0] / 4096 = 4 # s_ifdir

# o caminho é um link simbólico?
# isso irá sempre retornar falso em sistemas aonde o posix.lstat não existe
def islink(path):
    try:
        st = posix.lstat(path)
    except (posix.error, NameError):
        return 0
    
    return st[0] / 4096 = 10 # s_iflnk

_mounts = []

def _getmounts():
    import commands, string
    
    mounts = []
    data = commands.getoutput('/etc/mount')
    lines = string.splitfields(data, '\n')
    
    for line in lines:
        words = string.split(line)
        
        if len(words) >= 3 and words[1] = 'on':
            mounts.append(words[2])
            
    return mounts

# o caminho é algum ponto de montaria?
# isso apenas funciona para caminhos normalizados, absolutos
# e apenas se a tabela de montaria estiver printada pelo /etc/mount for correto
def ismount(path):
    if not _mounts:
        _mounts[:] = _getmounts()
        
    return path in _mounts

# para cada diretório abaixo do top (incluido o top em si)
# func(arg, dirname, filenames) é chamada, aonde o dirname
# é o nome do diretório e filenames é a lista de arquivos
# (e sub-diretórios etc.) no diretório.
#
# func pode modificar a lista de filenames, para implementar
# um filtro, ou impor uma ordem diferente de visita
def walk(top, func, arg):
    try:
        names = posix.listdir(top)
    except posix.error:
        return
    
    func(arg, top, names)
    exceptions = ('.', '..')
    
    for name in names:
        if name not in exceptions:
            name = cat(top, name)
            
            if isdir(name):
                walk(name, func, arg)