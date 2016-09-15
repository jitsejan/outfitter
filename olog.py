from time import gmtime, strftime
from datetime import datetime 
from pytz import timezone

def log(inputString, pType=None, color="white", style='no_effect'):
    if pType ==        'debug':
        color = 'blue'
        style = 'no_effect'
        inputString = '<b>Debug</b>\t' + inputString
    elif pType ==     'error':
        color = 'red'
        style = 'no_effect'
        inputString = '<b>Error</b>\t' + inputString
    elif pType ==     'warning':
        color = 'yellow'
        style = 'no_effect'
        inputString = '<b>Warning</b>\t' + inputString
    elif pType ==     'varHeader':
        color = 'purple'
        style = 'bold'
    elif pType ==     'info':
        color = 'green'
        style = 'no_effect'
        inputString = '<b>Info</b>\t' + inputString

    string_defs = {
        'startc'     : '\033[',
        'endc'         : '\033[0m'
    }
    color_defs = {
        'black'        : '30m',
        'red'        : '31m',
        'green'        : '32m',
        'yellow'     : '33m',
        'blue'        : '34m',
        'purple'    : '35m',
        'cyan'        : '36m',
        'white'        : '37m'
    }
    bg_defs = {
        'black_bg'    : '40m',
        'red_bg'    : '41m',
        'green_bg'    : '42m',
        'yellow_bg'    : '43m',
        'blue_bg'    : '44m',
        'purple_bg' : '45m',
        'cyan_bg'    : '46m',
        'white_bg'    : '47m'
    }
    style_defs = {
        'no_effect'    : '0',
        'bold'        : '1',
        'under'        : '4',
        'blink'        : '5',
        'inv'        : '7',
        'hidden'    : '8',
    }
   
    inputString = inputString.replace('<b>', string_defs['startc'] + style_defs['bold'] + ";" + color_defs[color])
    inputString = inputString.replace('</b>', string_defs['startc'] + style_defs[style] + ";" + color_defs[color])
    inputString = inputString.replace('<u>', string_defs['startc'] + style_defs['under'] + ";" + color_defs[color])
    inputString = inputString.replace('</u>', string_defs['startc'] + style_defs[style] + ";" + color_defs[color])
    inputString = inputString.replace('<i>', string_defs['startc'] + style_defs['inv'] + ";" + color_defs[color])
    inputString = inputString.replace('</i>', string_defs['startc'] + style_defs[style] + ";" + color_defs[color])
    
    amsterdam = timezone('Europe/Amsterdam')    
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    ams_time = datetime.now(amsterdam)
    nu = ams_time.strftime(fmt)
    
    print nu+ ' ' + string_defs['startc'] + style_defs[style] + ";" + color_defs[color] + inputString + string_defs['endc']