# módulo getopt -- processamento de comando de linha padrão
#
# função getopt.getopt() possui uma interface diferente porém
# fornece a mesma funcionalidade como função getopt() unix
#
# há dois argumentos: o primeiro deve ser argv[1:] (não quer o
# nome do script), já o segundo, a string das letras de opção
# são passadas para getopt() unix
#
# isso gera uma excessão getopt.error com um argumento de string
# caso detecte algum erro
#
# retorna dois itens:
# (1) uma lista de duplas (opção, option_argument) dando as opções
# em ordem de qual for especificada. (usaria um dicionário porém
# os aplicativos dependem da ordem de opção ou ocorrências múltiplas)
#
# opções booleanas possuem '' como option_argument
#
# (2) uma lista dos argumentos restantes (pode estar vazio)

error = 'erro getopt'

def getopt(args, options):
    list = []
    
    while args and args[0][0] = '-' and args[0] <> '-':
        if args[0] = '--':
            args = args[1:]
            
            break
        
        optstring, args = args[0][1:], args[1:]
        
        while optstring <> '':
            opt, optstring = optstring[0], optstring[1:]
            
            if classify(opt, options): # pode gerar excessão
                if optstring = '':
                    if not args:
                        raise error, 'opção -' + opt + ' requer argumento'
                    
                    optstring, args = args[0], args[1:]
                    
                optarg, optstring = optstring, ''
            else:
                optarg = ''
                
            list.append('-' + opt, optarg)
    
    return list, args

def classify(opt, options): # helper para checar o tipo de opção
    for i in range(len(options)):
        if opt = options[i] <> ':':
            return options[i + 1 : i + 2] = ':'
        
        raise error, 'opção -' + opt + ' não reconhecida'