#!/usr/bin/python3

from base64 import b64decode
from random import randint
from venomsrc.colored import Colors

colors = Colors()


def banner(version):  # select a random banner, and change <VERSION> for the argument passed

    banner1 = colors.HEADER + ''' 
  ____             _  __      __         ___            
 |  _ \           | | \ \    / /        / _ \           
 | |_) | __ _  ___| | _\ \  / /__ _ __ | | | |_ __ ___  
 |  _ < / _` |/ __| |/ /\ \/ / _ \ '_ \| | | | '_ ` _ \ 
 | |_) | (_| | (__|   <  \  /  __/ | | | |_| | | | | | |
 |____/ \__,_|\___|_|\_\  \/ \___|_| |_|\___/|_| |_| |_|
''' + colors.ENDC + '''  
Version: <VERSION>       << The Exploitation Swiss Army knife >>
-------------------------------------------------------------------
'''

    banner2 = ''' 

 ___________
< ''' + colors.WARNING + "Backven0m!" + colors.ENDC + ''' >
 -----------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\ \n                ||----w |
                ||     ||

Version: <VERSION>      << The Exploitation Swiss Army knife >>
------------------------------------------------------------------
'''

    banner3 = colors.BOLD + '''

______            _     _   _            _____           
| ___ \          | |   | | | |          |  _  |          
| |_/ / __ _  ___| | _ | | | | ___ _ __ | |/' |_ __ ___  
| ___ \/ _` |/ __| |/ /  | | |/ _ \ '_ \|  /| | '_ ` _ \ 
| |_/ / (_| | (__|   < \ \_/ /  __/ | | \ |_/ / | | | | |
\____/ \__,_|\___|_|\_\ \___/ \___|_| |_|\___/|_| |_| |_|
''' + colors.ENDC + '''
Version: <VERSION>               << The Exploitation Swiss Army knife >>
------------------------------------------------------------------------------
'''

    banner4 = ''' 

   (                 )                         )         
 ( )\     )       ( /(  (   (    (          ( /(    )    
 )((_) ( /(   (   )\()) )\  )\  ))\  (      )\())  (     
((_)_  )(_))  )\ ((_)\ ((_)((_)/((_) )\ )  ((_)\   )\  ' 
 | _ )((_)_  ((_)| |(_)\ \ / /(_))  _(_/(  /  (_)_((_))  
 | _ \/ _` |/ _| | / /  \ V / / -_)| ' \))| () || '  \() 
 |___/\__,_|\__| |_\_\   \_/  \___||_||_|  \__/ |_|_|_|  

Version: <VERSION>      << The Exploitation Swiss Army knife >>
-------------------------------------------------------------------------
'''

    banner5 = colors.OKCYAN + '''                                            
 _____         _   _____         ___       
| __  |___ ___| |_|  |  |___ ___|   |_____ 
| __ -| .'|  _| '_|  |  | -_|   | | |     |
|_____|__,|___|_,_|\___/|___|_|_|___|_|_|_|
''' + colors.ENDC + '''
Version: <VERSION>     << The Exploitation Swiss Army knife >>
------------------------------------------------------------------
'''

    banner6 = '\n' + colors.OKGREEN + b64decode(
        'IOKWhOKWhOKWhOKWhCAgICDiloTiloTiloQgICAgICAg4paE4paI4paI4paI4paI4paEICAg4paI4paIIOKWhOKWiOKWgOKWiOKWiOKWkiAgIO'
        'KWiOKWk+KWk+KWiOKWiOKWiOKWiOKWiCAg4paI4paI4paI4paEICAgIOKWiCAg4paS4paI4paI4paI4paI4paIICAg4paI4paI4paI4paEIOKWh'
        'OKWiOKWiOKWiOKWkwrilpPilojilojilojilojilojiloQg4paS4paI4paI4paI4paI4paEICAgIOKWkuKWiOKWiOKWgCDiloDiloggICDiloji'
        'lojiloTilojilpLilpPilojilojilpEgICDilojilpLilpPiloggICDiloAgIOKWiOKWiCDiloDiloggICDilogg4paS4paI4paI4paSICDiloj'
        'ilojilpLilpPilojilojilpLiloDilojiloAg4paI4paI4paSCuKWkuKWiOKWiOKWkiDiloTilojilojilpLilojiloggIOKWgOKWiOKWhCAg4p'
        'aS4paT4paIICAgIOKWhCDilpPilojilojilojiloTilpEg4paT4paI4paIICDilojilpLilpHilpLilojilojiloggICDilpPilojiloggIOKWg'
        'OKWiCDilojilojilpLilpLilojilojilpEgIOKWiOKWiOKWkuKWk+KWiOKWiCAgICDilpPilojilojilpEK4paS4paI4paI4paR4paI4paAICDi'
        'lpHilojilojiloTiloTiloTiloTilojilogg4paS4paT4paT4paEIOKWhOKWiOKWiOKWkuKWk+KWiOKWiCDilojiloQgIOKWkuKWiOKWiCDiloj'
        'ilpHilpHilpLilpPiloggIOKWhCDilpPilojilojilpIgIOKWkOKWjOKWiOKWiOKWkuKWkuKWiOKWiCAgIOKWiOKWiOKWkeKWkuKWiOKWiCAgIC'
        'DilpLilojiloggCuKWkeKWk+KWiCAg4paA4paI4paTIOKWk+KWiCAgIOKWk+KWiOKWiOKWkuKWkiDilpPilojilojilojiloAg4paR4paS4paI4'
        'paI4paSIOKWiOKWhCAg4paS4paA4paI4paRICDilpHilpLilojilojilojilojilpLilpLilojilojilpEgICDilpPilojilojilpHilpEg4paI'
        '4paI4paI4paI4paT4paS4paR4paS4paI4paI4paSICAg4paR4paI4paI4paSCuKWkeKWkuKWk+KWiOKWiOKWiOKWgOKWkiDilpLilpIgICDilpPi'
        'lpLilojilpHilpEg4paR4paSIOKWkiAg4paR4paSIOKWkuKWkiDilpPilpIgIOKWkSDilpDilpEgIOKWkeKWkSDilpLilpEg4paR4paRIOKWkuKW'
        'kSAgIOKWkiDilpIg4paRIOKWkuKWkeKWkuKWkeKWkuKWkSDilpEg4paS4paRICAg4paRICDilpEK4paS4paR4paSICAg4paRICAg4paSICAg4pa'
        'S4paSIOKWkSAg4paRICDilpIgICDilpEg4paR4paSIOKWkuKWkSAg4paRIOKWkeKWkSAgIOKWkSDilpEgIOKWkeKWkSDilpHilpEgICDilpEg4p'
        'aS4paRICDilpEg4paSIOKWkuKWkSDilpEgIOKWkSAgICAgIOKWkQog4paRICAgIOKWkSAgIOKWkSAgIOKWkiAgIOKWkSAgICAgICAg4paRIOKWk'
        'eKWkSDilpEgICAgIOKWkeKWkSAgICAg4paRICAgICAg4paRICAg4paRIOKWkSDilpEg4paRIOKWkSDilpIgIOKWkSAgICAgIOKWkSAgIAog4paR'
        'ICAgICAgICAgICAg4paRICDilpHilpEg4paRICAgICAg4paRICDilpEgICAgICAgIOKWkSAgICAg4paRICDilpEgICAgICAgICDilpEgICAgIOK'
        'WkSDilpEgICAgICAgICDilpEgICAKICAgICAg4paRICAgICAgICAgICDilpEgICAgICAgICAgICAgICAgICAg4paRICAgICAgICAgICAgICAgIC'
        'AgICAgICAgICAgICAgICAgICAgICAgICAKCg==').decode("utf-8") + colors.ENDC + '''
Version: <VERSION>        << The Exploitation Swiss Army knife >>
--------------------------------------------------------------------'''

    try:
        banners = [banner1, banner2, banner3, banner4, banner5, banner6, banner6, banner6, banner6]
        print(banners[randint(0, len(banners))].replace('<VERSION>', version))
    except:
        print(banner1.replace('<VERSION>', version))
