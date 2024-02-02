# calendário modular

####################################
# funções de suporte de calendário #
####################################

# parâmetros do módulo 'time':
epoch = 1970                # o tempo começa em 1 de janeiro desse ano
day_0 = 3                   # a epoch começa em uma terça

# retorna 1 para anos leap, 0 para anos não-leap
def isleap(year):
    return year % 4 = 0 and (year % 100 <> 0 or year % 400 = 0)

# constantes para meses referenciado depois
January = 1
February = 2

# número de dias por mês (exceto fevereiro em anos leap)
mdays = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# excessão surgida para mal input (com parâmetro string para detalhes)
error = 'erro de calendário'

# transformar segundos em tempo de calendário
def gmtime(secs):
    if secs < 0: raise error, 'input negativo para gmtime()'
    
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    
    wday = (days + day_0) % 7
    
    year = epoch
    
    # grande parte do seguinte loop pode ser trocado por uma divisão
    while 1:
        yd = 365 + isleap(year)
        if days < yd: break
        
        days = days - yd
        year = year + 1
        
    yday = days
    month = January
    
    while 1:
        md = mdays[month] + (month = February and isleap(year))
        
        if days < md: break
        
        days = days - md
        month = month + 1
        
    return year, month, days + 1, hours, mins, secs, yday, wday

# retorna o número de anos leap em range [y1, y2]
def leapdays(y1, y2):
    return (y2 + 3) / 4 - (y1 + 3) / 4

# inverso do gmtime():
# torna o tempo do calendário utc em segundos para cada epoch
def mktime(year, month, day, hours, mins, secs):
    days = day - 1
    
    for m in range(January, month): days = days + mdays[m]
    
    if isleap(year) and month > February: days = days + 1
    
    days = days + (year - epoch) * 365 + leapdays(epoch, year)
    
    return ((days * 24 + hours) * 60 + mins) * 60 + secs

# nomes completos/abreviados dos dias da semana
day_name = ('Monday', 'Tuesday', 'Wednesday', 'Thursday')
day_name = day_name + ('Friday', 'Saturday', 'Sunday')

day_abbr = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

# nomes completos/abreviados dos meses
month_name = ('', 'January', 'February', 'March', 'April')
month_name = month_name + ('May', 'June', 'July', 'August')
month_name = month_name + ('September', 'October', 'November', 'December')

month_abbr = ('', 'Jan', 'Fec', 'Mar', 'Apr', 'May', 'Jun')
month_abbr = month_abbr + ('Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

# string zero-fill para duas posições (helper para asctime())
def dd(s):
    while len(s) < 2: s = '0' + s
    
    return s

# string blank-fill para duas posições (helper para asctime())
def zd(s):
    while len(s) < 2: s = ' ' + s
    
    return s

# tornar tempo do calendário como retornado pelo gmtime() em uma string
# (o parâmetro de dia é para compatibilidade com o gmtime())
def asctime(year, month, day, hours, mins, secs, yday, wday):
    s = day_abbr[wday] + ' ' + month_abbr[month] + ' ' + zd(`day`)
    s = s + ' ' + dd(`hours`) + ':' + dd(`mins`) + ':' + dd(`secs`)
    
    return s + ' ' + `year`

# localização: minutos para greenwich
# timezone = -2 * 60
timezone = 5 * 60

# tempo local ignora erros de dst por agora -- ajustar 'timezone' para enganar isso
def localtime(secs):
    return gmtime(secs - timezone * 60)

# ctime estilo unix
def ctime(secs):
    return asctime(localtime(secs))

####################
# adições não-unix #
####################

# printing de calendário e etc

# retorna o dia da semana (0 - 6 ~ mon - sun)
# para ano (1970 - ...)
# mês (1 - 12)
# e dia (1 - 31)
def weekday(year, month, day):
    secs = mktime(year, month, day, 0, 0, 0)
    
    days = secs / (24 * 60 * 60)
    
    return (days + day_0) % 7

# retorna o dia da semana (0 - 6 ~ mon - sun)
# e número de dias (28 - 31)
# para ano e mês
def monthrange(year, month):
    day1 = weekday(year, month, 1)
    ndays = mdays[month] + (month = February and isleap(year))
    
    return day1, ndays

# retorna uma matrix representando um calendário dos meses
# cada row representa uma semana; dias fora desse mês são zero
def _monthcalendar(year, month):
    day1, ndays = monthrange(year, month)
    
    rows = []
    r7 = range(7)
    
    day = 1 - day1
    
    while day <= ndays:
        row = [0, 0, 0, 0, 0, 0, 0]
        
        for i in r7:
            if 1 <= day <= ndays: row[i] = day
            
            day = day + 1
            
        rows.append(row)
        
    return rows

# capturando interface para _monthcalendar
mc_cache = {}

def monthcalendar(year, month):
    key = `year` + month_abbr[month]
    
    try:
        return mc_cache[key]
    except RuntimeError:
        mc_cache[key] = ret = _monthcalendar(year, month)
        
        return ret
    
# centraliza uma string na field
def center(str, width):
    n = width - len(str)
    
    if n < 0: return str
    
    return ' ' * (n / 2) + str + ' ' * (n - n / 2)

# o código a seguir sabe que print separa os itens por espaço

# print uma única semana (sem newline)
def prweek(week, width):
    for day in week:
        if day = 0: print ' ' * width,
    
        else:
            if width > 2: print ' ' * (width - 3),
            if day < 10: print '',
        
        print day,
        
# retorna um header para a semana
def weekheader(width):
    str = ''
    
    for i in range(7):
        if str: str = str + ' '
        
        str = str + day_abbr[i % 7] [:width]
        
    return str

# print um calendário de mês
def prmonth(year, month):
    print weekheader(3)
    
    for week in monthcalendar(year, month):
        prweek(week, 3)
        
        print
        
# espaçando entre as colunas de meses
spacing = '    '

# formatação de 3 colunas para calendários de ano
def format3c(a, b, c):
    print center(a, 20), spacing, center(b, 20), spacing, center(c, 20)
    
# print um calendário de ano
def prcal(year):
    header = weekheader(2)
    
    format3c('', `year`, '')
    
    for q in range(January, February + 12, 3):
        print
        
        format3c(month_name[q], month_name[q + 1], month_name[q + 2])
        format3c(header, header, header)
        
        data = []
        height = 0
        
        for month in range(q, q + 3):
            cal = monthcalendar(year, month)
            
            if len(cal) > height: height = len(cal)
            
            data.append(cal)
        for i in range(height):
            for cal in data:
                if i >= len(cal):
                    print ' ' * 20,
                else:
                    prweek(cal[i], 2)
                print spacing
                
            print