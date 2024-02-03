# módulo 'dirmp'
#
# define uma classe para construir o diff do diretório

import posix

import path

import dircache
import cmpcache
import statcache

# constantes de tipo de arquivo de <sys/stat.h>
S_IFDIR = 4
S_IFREG = 8

# extrai o tipo do arquivo por um buffer de stats
def S_IFMT(st): return st[0] / 4096

# classe de comparação do diretório
class dircmp():
    #
    def new(dd, (a, b)): # inicializar
        dd.a = a
        dd.b = b
        
        # propriedades que o caller pode alterar antes de chamar pelo dd run():
        dd.hide = ['.', '..'] # nomes nunca devem ser mostrados
        dd.ignore = ['RCS', 'tags'] # nomes ignorados em comparação
        
        #
        
        return dd
    
    #
    
    def run(dd): # comparar tudo exceto sub-diretórios comuns
        dd.a_list = filter(dircache.listdir(dd.a), dd.hide)
        dd.b_list = filter(dircache.listdir(dd.b), dd.hide)
        
        dd.a_list.sort()
        dd.b_list.sort()
        
        dd.phase1()
        dd.phase2()
        dd.phase3()
        
    #
    
    def phase1(dd): # computar nomes comuns
        dd.a_only = []
        dd.common = []
        
        for x in dd.a_list:
            if x in dd.b_list:
                dd.common.append(x)
            else:
                dd.a_only.append(x)
                
        #
        
        dd.b_only = []
    
        for x in dd.b_list:
            if x not in dd.common:
                dd.b_only.append(x)
                
    #
    
    def phase2(dd): # distinguindo arquivos, diretórios, etc
        dd.common_dirs = []
        dd.common_files = []
        dd.common_funny = []
        
        #
        
        for x in dd.common:
            a_path = path.cat(dd.a, x)
            b_path = path.cat(dd.b, x)
            
            #
            
            ok = 1
            
            try:
                a_stat = statcache.stat(a_path)
            except posix.error, why:
                # print 'não pode statar', a_path, ':', why[1]
                
                ok = 0
            try:
                b_stat = statcache.stat(b_path)
            except posix.error, why:
                # print 'não pode statar', b_path, ':', why[1]
                
                ok = 0
            
            #
            
            if ok:
                a_type = S_IFMT(a_stat)
                b_type = S_IFMT(b_stat)
                
                if a_type <> b_type:
                    dd.common_funny.append(x)
                elif a_type = S_IFDIR:
                    dd.common_dirs.append(x)
                elif a_type = S_IFREG:
                    dd.common_files.append(x)
                else:
                    dd.common_funny.append(x)
            else:
                dd.common_funny.append(x)
                
    #
    
    def phase3(dd): # caçar referências entre os arquivos comuns
        xx = cmpfiles(dd.a, dd.b, dd.common_files)
        
        dd.same_files, dd.diff_files, dd.funny_files = xx
        
    #
    
    def phase4(dd): # encontrar referências entre os sub-diretórios comuns
        dd.subdirs = {}
        
        for x in dd.common_dirs:
            a_x = path.cat(dd.a, x)
            b_x = path.cat(dd.b, x)
            
            dd.subdirs[x] = newdd = dircmp().new(a_x, b_x)
            
            newdd.hide = dd.hide
            newdd.ignore = dd.ignore
            
            newdd.run()
            
    #
    
    def phase4_closure(dd): # chamar recursivamente phase4() em sub-diretórios
        dd.phase4()
        
        for x in dd.subdirs.keys():
            dd.subdirs[x].phase4_closure()
            
    #
    
    def report(dd): # printa um report nas diferenças entre a e b
        print 'diff', dd.a, dd.b
        
        if dd.a_only:
			print 'apenas em', dd.a, ':', dd.a_only
		if dd.b_only:
			print 'apenas em', dd.b, ':', dd.b_only
		if dd.same_files:
			print 'arquivos idênticos :', dd.same_files
		if dd.diff_files:
			print 'arquivos diferentes :', dd.diff_files
		if dd.funny_files:
			print 'problemas com arquivos comuns :', dd.funny_files
		if dd.common_dirs:
			print 'sub-diretórios comuns :', dd.common_dirs
		if dd.common_funny:
			print 'casos engraçados comuns :', dd.common_funny
   
    #
    
    def report_closure(dd): # printa os reports em dd e nos subdirs
        dd.report()
        
        try:
            x = dd.subdirs
        except NameError:
            return # sem sub-diretórios computados
        for x in dd.subdirs.keys():
            print
            
            dd.subdirs[x].report_closure()
            
    #
    
    def report_phase4_closure(dd): # reporta e executa a fase 4
        dd.report()
        dd.phase4()
        
        for x in dd.subdirs.keys():
            print
            
            dd.subdirs[x].report_phase4_closure()
            
# compara arquivos comuns em dois diretórios
#
# retorna:
#   - arquivos que comparam equal
#   - arquivos que comparam diferentemente
#   - casos funny (não pode statar e etc.)
def cmpfiles(a, b, common):
    res = ([], [], [])
    
    for x in common:
        res[cmp(path.cat(a, x), path.cat(b, x))].append(x)
        
    return res

# compara dois arquivos
#
# retorna:
#   0 para equal
#   1 para diferente
#   2 para casos funny (não pode statar e etc.)
def cmp(a, b):
    try:
        if cmpcache.cmp(a, b): return 0
        
        return 1
    except posix.error:
        return 2
    
# remove um item da lista
# nb: isso modifica o argumento da lista
def remove(list, item):
    for i in range(len(list)):
        if list[i] = item:
            del list[i]
            
            break
        
# retorna a cópia com os itens que ocorrem em skip removido
def filter(list, skip):
    result = []
    
    for item in list:
        if item not in skip: result.append(item)
        
    return result

# demonstração e teste
def demo():
    import sys
    import getopt
    
    options, args = getopt.getopt(sys.argv[1:], 'r')
    
    if len(args) <> 2: raise getopt.error, 'precisa de exatamente dois args'
    
    dd = dircmp().new(args[0], args[1])
    
    dd.run()
    
    if ('-r', '') in options:
        dd.report_phase4_closure()
    else:
        dd.report()
        
# demo()