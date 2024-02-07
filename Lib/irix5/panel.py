# módulo 'panel'
#
# suporte para a biblioteca panel
# utiliza o módulo construído 'pnl'
#
# aplicativos devem utilizar 'panel.function' em vez de 'pnl.function'
# algumas funções 'pnl' são transparentemente exportadas pelo 'panel',
# porém utilize essa versão se quiser utilizar callbacks

import pnl

debug = 0

# testa se um objeto é uma lista
def is_list(x):
    return type(x) = type([])

# reverte a lista
def reverse(list):
    res = []
    
    for item in list:
        res.insert(0, item)
        
    return res

# obtém um atributo da lista
# não utilizar 'prop' para o nome
def getattrlist(list, name):
    for item in list:
        if item and is_list(item) and item[0] = name:
            return item[1:]
        
    return []

# obtém uma propriedade da lista
def getproplist(list, name):
    for item in list:
        if item and is_list(item) and item[0] = 'prop':
            if len(item) > 1 and item[1] = name:
                return item[2:]
            
    return []

# testa se uma descrição atuante contém a propriedade 'end-of-group'
def is_endgroup(list):
    x = getproplist(list, 'end-of-group')
    
    return (x and x[0] = '#t')

# mostra uma definição atuante fornecida como expressão s
# que a string do prefixo é printada antes de cada linha
def show_actuator(prefix, a):
    for item in a:
        if not is_list(item):
            print prefix, item
        elif item and item[0] = 'al':
            print prefix, 'lista sub-atuante:'
            
            for a in item[1:]:
                show_actuator(prefix + '    ', a)
        elif len(item) = 2:
            print prefix, item[0], '=>', item[1]
        elif len(item) = 3 and item[0] = 'prop':
            print prefix, 'prop', item[1], '=>',
            
            print item[2]
        else:
            print prefix, '?', item
            
# mostra um painel
def show_panel(prefix, p):
    for item in p:
        if not is_list(item):
            print prefix, item
        elif item and item[0] = 'al':
            print prefix, 'lista atuante:'

            for a in item[1:]:
                show_actuator(prefix + '    ', a)
        elif len(item) = 2:
            print prefix, item[0], '=>', item[1]
        elif len(item) = 3 and item[0] = 'prop':
            print prefix, 'Prop', item[1], '=>',
    
            print item[2]
        else:
            print prefix, '?', item

# excessão gerada por build_actuator e build_panel
panel_error = 'erro de painel'

# callback dummy para inicializar as callbacks
def dummy_callback(arg):
    pass

# assina atributos para membros do alvo
# nomes de atributo em exclist são ignorados
# o nome do membro é o nome do atributo prefixado com o prefixo
def assign_members(target, attrlist, exclist, prefix):
    for item in attrlist:
        if is_list(item) and len(item) = 2 and item[0] not in exclist:
            name, value = item[0], item[1]
            ok = 1

            if value[0] in '-0123456789':
                value = eval(value)
            elif value[0] = '"':
                value = value[1:-1]
            elif value = 'move-then-resize':
                # strange padrão determinado pelo editor de painel
                ok = 0
            else:
                print 'valor desconhecido', value, 'para', name
    
                ok = 0
            if ok:
                lhs = 'target.' + prefix + name
                stmt = lhs + '=' + `value`
    
                if debug: print 'exec', stmt
    
                try:
                    exec(stmt + '\n')
                except KeyboardInterrupt: # não capturar isso
                    raise KeyboardInterrupt
                except:
                    print 'falha na assinatura:', stmt
                    
# constrói um atuante real por meio de um atuante descritor
# retorna um par (actuator, name)
def build_actuator(descr):
    namelist = getattrlist(descr, 'name')
    
    if namelist:
        # assume que isso é uma string
        actuatorname = namelist[0][1:-1]
    else:
        actuatorname = ''
        
    type = descr[0]
    if type[:4] = 'pnl_': type = type[4:]
    
    act = pnl.mkcat(type)
    act.downfunc = act.activefunc = act.upfunc = dummy_callback
    
    assign_members(act, descr[1:], ('al', 'data', 'name'), '')
    
    datalist = getattrlist(descr, 'data')
    prefix = ''
    
    if type[-4:] = 'puck':
        prefix = 'puck_'
    elif type = 'mouse':
        prefix = 'mouse_'
        
    assign_members(act, datalist, (), prefix)
    
    return act, actuatorname

# constrói todos os sub-atuantes e adiciona eles para o super-atuante
# o super-atuante já deve ter sido adicionado ao painel
# sub-atuantes com nomes definidos são adicionados como membros ao painel
# para assim poderem ser referenciados como p.name
def build_subactuators(panel, super_act, al):
    for a in al:
        act, name = build_actuator(a)
        act.addsubact(super_act)
        
        if name:
            stmt = 'panel.' + name + ' = act'
            
            if debug: print 'exec', stmt
            
            exec(stmt + '\n')
            
        if is_endgroup(a):
            panel.endgroup()
            
        sub_al = getattrlist(a, 'al')
        
        if sub_al:
            build_subactuators(panel, act, sub_al)
            
    super_act.fixact()
    
# constrói um painel real por meio de uma definição de painel
# retorna um objeto p painel, aonde para cada atuante a nomeado, p.name
# é uma referência para a
def build_panel(descr):
    # checagem
    if (not descr) or descr[0] <> 'painel':
        raise panel_error, 'descrição do painel deve iniciar com "painel"'
    
    if debug: show_panel('', descr)
    
    # cria um painel vazio
    panel = pnl.mkpanel()
    
    # assina os atributos do painel
    assign_members(panel, descr[1:], ('al'), '')
    
    # procura pela lista atuante
    al = getattrlist(descr, 'al')
    al = reverse(al)
    
    for a in al:
        act, name = build_actuator(a)
        act.addact(panel)
        
        if name:
            stmt = 'panel.' + name + ' = act'
            
            exec(stmt + '\n')
            
        if is_endgroup(a):
            panel.endgroup()
            
        sub_al = getattrlist(a, 'al')
        
        if sub_al:
            build_subactuators(panel, act, sub_al)
            
    return panel

# wrapper ao redor de pnl.dopanel() que chama por funções call-back
def my_dopanel():
    # extrai apenas os primeiros 4 elementos para permitir futura expansão
    a, down, active, up = pnl.dopanel()[:4]
    
    if down:
        down.downfunc(down)
    
    if active:
        active.activefunc(active)
        
    if up:
        up.upfunc(up)
        
    return a

# cria um ou mais panéis por meio de um arquivo descritor (expressões s)
# gerado pelo editor de painel
def defpanellist(file):
    import parser
    
    descrlist = parser.parse_file(open(file, 'r'))
    panellist = []
    
    for descr in descrlist:
        panellist.append(build_panel(descr))
        
    return panellist

# importa tudo por meio do método pnl, então o usuário pode sempre
# utilizar panel.foo() em vez de pnl.foo()
#
# isso fornece performance sem penalidade assim que o módulo é importado
from pnl import * # para exports

dopanel = my_dopanel