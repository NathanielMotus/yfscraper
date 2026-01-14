import locale

locale.setlocale(locale.LC_ALL,'')

def parse_financials_number(element):
    number=element.text
    # delete non-breaking spaces
    number=number.replace("\u202f","")
    # replace "--" by "0"
    number=number.replace("--","0")
    # return number*1000
    return int(locale.atof(number)*1000)

def parse_stat_number(element):
    locale.setlocale(locale.LC_ALL,'')
    number=element.text
    factor=1

    # récupère le multiplicateur et l'efface
    if number[-1]=="K" or number[-1]=="k":
        factor=1000
        number=number[:-1]
    elif number[-1]=='M':
        factor=1000000
        number=number[:-1]
    elif number[-1]=="B":
        factor=1000000000
        number=number[:-1]
    elif number[-1]=="s":
        factor=1000000000
        number=number[:-3]
    
    # retourne le nombre multiplié par le facteur, arrondi à l'entier le plus proche
    return float(locale.atof(number)*factor)