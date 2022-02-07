"""Ici je joue un peu avec gtts, l'histoire d'apprendre ce qui est possible."""
import os
import re
import numpy as np
from langdetect import detect
from gtts import gTTS
from random import shuffle

# TODO: Functies maken voor de overgang ruwe woordjes => txt-overzichten.
#       Regarder sous quelle forme on peut récupérer des mots,
#       regarder quelle serait la meilleure façon de les enregistrer.
#       (Des fichiers .txt ou autrement?)
#       De module translate gebruiken of iets anders?
#       deze lijkt best goed te werken, maar heeft een vertaalbegrenzing.
#       Misschien toch woordjes handmatig invoeren.
#       Misschien Guillhermo of andere mensen vragen of ze lijstjes hebben.

def leesParenTXT(pad):
    """
    Stuurt van een tekstbestand (met pad vanaf "overhoormap") van de vorm
    tekst1          tekst2
    ...             ...
    tekst(2N-1)     tekst2N
    een parenlijst van de vorm:
    [(tekst1, tekst2), ..., (tekst(2N-1), tekst2N)]
    terug.
    We gebruiken deze functie vooral om woordoverzichten op te halen.
    """
    with open('{}.txt'.format(pad), 'r') as parenTXT:
        inhoud = parenTXT.read()
    regels = re.split("\n+",inhoud)
    paren = []
    for regel in regels:
        paar = re.split("\t+", regel)
        paren.append(tuple(paar))
    return paren

# Ik twijfel echt wat ik met deze functie moet.
# Aan de ene kant vind ik het netjes hem apart te definiëren,
# aan de andere kant vind ik het echt superdom.

##def leesOverzicht(naam):
##    """
##    Voert leesParenTXT uit in ons specifieke geval.
##    Leest een overzicht van woorden en maakt er een parenlijst van.
##    """
##    pad = "txt-overzichten\\{}".format(naam)
##    return leesParenTXT(pad)


def schrijfParenTXT(paren, pad):
    """
    Maakt van een parenlijst van de vorm:
    [(tekst1, tekst2), ..., (tekst(2N-1), tekst2N)]
    een tekstbestand van de vorm:
    tekst1          tekst2
    ...             ...
    tekst(2N-1)     tekst2N
    en slaat deze op op het aangegeven adrs (vanaf overhoormap.)
    We gebruiken deze functie vooral om stamplijsten op te schrijven.
    """
    lenMax = max([len(paar[0]) for paar in paren]) # De max lengte links.
    with open('{}.txt'.format(pad), 'w') as parenTXT:
        for paar in paren:
            nTabs = int(np.ceil(lenMax/8) - np.floor(len(paar[0])/8)) + 1
            temp = paar[0] + "\t"*nTabs + paar[1] + "\n"
            parenTXT.write(temp)

# -----------------------------------------------------------

def dictList(dico):
    """dico in, lijst van paren uit."""
    return [(clef, dico[clef]) for clef in dico.keys()]

def listDic(lijst):
    """lijst van paren in, dico uit."""
    dico = {}
    for (links, rechts) in lijst:
        dico[links] = rechts
    return dico

# -----------------------------------------------------------

def maakLabel(paren, nummer):
    """TODO: décire ce truc-là."""
    nCijfers = len(str(2*len(paren)))
    nNullen = nCijfers - len(str(nummer))
    nummerLabel = nNullen*"0" + str(nummer)
    return nummerLabel

# TODO: Essayer cette fonction.
def bepaalTalen(paren):
    """
    Stuurt van een parenlijst de linker- en rechtertaal terug.
    Werkt alleen als de lijsten lang genoeg zijn,
    en uiteraard mag een kolom maar uit één taal bestaan.
    """
    stringLinks = ""
    stringRechts = ""
    for paar in paren:
        stringLinks += paar[0] + ", "
        stringRechts += paar[1] + ", "
    stringLinks = stringLinks[:-2]
    stringRechts = stringRechts[:-2]
    return detect(stringLinks), detect(stringRechts) 

def maakStamplijst(dico, n):
    """
    Maakt een n-voudige stamplijst van het aangegeven woordenboek,
    (of parenlijst) en stuurt deze terug.
    """
    if type(dico) is dico: # Als lijst ingevoerd al oké.
        lijst = dictList(dico)
    stampLijst = []
    for k in range(n):
        random.shuffle(lijst)
        stampLijst += lijst
    return stampLijst

# TODO: Kijken of dit werkt.
#       Ook kijken of het luisterbaar is, of dat er moet worden bijgeschaafd.
#       Hiervoor een testversie gebruiken, en vooral voor de latijnlijst.
def maakMP3map(paren, naam):
    """TODO: décrire ce truc-là."""
    os.mkdir("mp3-fragmenten\\" + naam)
    taalLinks, taalRechts = bepaalTalen(paren) # Het paar talen.
    teller = 1
    for paar in paren:
        padLeeg = "mp3-fragmenten\\{}\\{}{}.mp3"
        pad = padLeeg.format(naam, maakLabel(paren, teller), paren[0])
        tts = gTTS(paar[0], lang=taalLinks, slow=True)
        tts.save(pad)
        teller += 1
        pad = padLeeg.format(naam, maakLabel(paren, teller), paren[1])
        tts = gTTS(paar[1], lang=taalRechts, slow=True)
        tts.save(pad)
        teller += 1

# TODO: Een functie die maakStamplijst en maakMP3map mooi combineert.
#       Hier moet alles met naamgeving gebeuren.

# ----------------------------------------------------------------

if __name__ == "__main__":

    # Een testlijst:
    lijst = []
    lijst.append(("tekst" , "pieuw"))
    lijst.append(("teksawetwergegheght" , "pieuwtawerge"))
    lijst.append(("teksawetwerg" , "pieuwtawerge"))
    lijst.append(("teksawrg" , "pieuwtawerge"))
    lijst.append(("teksawetwergegheghtasger" , "pieuwtawerge"))
    lijst.append(("teksawetwersger" , "eaergegpieuwtawerge"))
    schrijfParenTXT(lijst, "stinkie")

    lijst = []
    for k in range(200):
        lijst.append(("pief", "paf"))

    paren = leesParenTXT("txt-overzichten\\Latijn")
    print(bepaalTalen(paren))
    
    print("Ici nous allons encore faire quelques essais.")

# TODO: Lezen wat de optatieve parameters doen in de module gTTS.
#       Misschien zitten er nuttige mogelijkheden tussen.
