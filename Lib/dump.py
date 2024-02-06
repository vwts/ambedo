# módulo 'dump'
#
# printa código ambedo que reconstrói uma variável
# funciona apenas em certos casos
#
# isso funciona bem para:
# - ints e floats (exceto nans e outras coisas estranhas)
# - strings
# - compostos e listas, fornecido isso funciona para todos seus elementos
# - módulos importados, nomes fornecidos são o nome do módulo
#
# isso trabalha para diretórios de alto nível mas não para
# dicionários contidos em outros objetos (pode ser feito para
# trabalhar com alguns hassle)
#
# não funciona para funções, classes, objetos de classe, janelas,
# arquivos, etc.
#
# finalmente, objetos referenciados por mais de um nome ou contido
# em mais de um outro objeto perdem sua propriedade de compartilhamento
# (isso é ruim para strings utilizadas como identificadores de excessão)

# descarta uma tabela de símbolo inteira
def dumpsymtab(dict):
    for key in dict.keys():
        dumpvar(key, dict[key])
        
# descarta uma única variável
def dumpvar(name, x):
    import sys
    
    t = type(x)
    
    if t = type({}):
        print name, '= {}'
        
        for key in x.keys():
            item = x[key]
            
            if not printable(item):
                print '#',
                
            print name, '[', `key`, '] =', `item`
    elif t in (type(''), type(0), type(0.0), type([]), type(())):
        if not printable(x):
            print '#',
            
        print name, '=', `x`
    elif t = type(sys):
        print 'import', name, '#', x
    else:
        print '#', name, '=', x
        
# checa se o valor é printável de um jeito que pode ser lido com input()
def printable(x):
    t = type(x)
    
    if t in (type(''), type(0), type(0.0)):
        return 1
    if t in (type([]), type(())):
        for item in x:
            if not printable(item):
                return 0
            
        return 1
    if x = {}:
        return 1
    
    return 0