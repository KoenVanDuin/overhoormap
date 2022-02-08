"""Hier speel ik een beetje met gtts, gewoon om uit te vinden wat er mogelijk is."""

import os
import re
import random
import numpy as np
from langdetect import detect
from gtts import gTTS
from random import shuffle
from shutil import rmtree, copyfile

# TODO: Met googletrans spelen.
#       In het bijzonder kijken of taaldetectie werkt.
#       Als dat klopt, dan langid désinstalleren.

# TODO: Zodra de tijd rijp is proberen taaldetectiefunctie te maken, met langid.
#       Als geen antwoord op GitHub, kijken of langid voor ons plan goed werkt.
#       (Dit wil zeggen met massa's van tientallen of honderden losse woordjes.)

# ---------------------------------------------
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
    """
    lijst van paren in, dico uit.
    WARNUNG: gooit paren weg met dubbele linkerkanten.    """
    dico = {}
    for (links, rechts) in lijst:
        dico[links] = rechts
    return dico

# -----------------------------------------------------------

def maakLabel(paren, nummer):
    """
    Formatteert nummers (bijv 12) tot strings (bijv '0012').
    Het aantal nullen is zo gekozen dat alle nummers uit
    even veel cifjers bestaan.
    WARNUNG:    We gaan zit beest binnenkort verwijderen omdat deze overbodig is gebleken.
    """
    raise NotImplementedError
    nCijfers = len(str(2*len(paren)))
    nNullen = nCijfers - len(str(nummer))
    nummerLabel = nNullen*"0" + str(nummer)
    return nummerLabel

# WARNUNG: Deze functie gaat waarschijnlijk de prullenbak in.
def bepaalTalen(paren):
    """
    Stuurt van een parenlijst de linker- en rechtertaal terug.
    Werkt alleen als de lijsten lang genoeg zijn,
    en uiteraard mag een kolom maar uit één taal bestaan.
    WARNUNG:    Dit werkt niet goed met de huidige taaldetector.
                Daarom gebruiken we deze functie niet zolang we geen
                goede vinden kunnen.
    """
    raise NotImplementedError
    stringLinks = ""
    stringRechts = ""
    for paar in paren:
        stringLinks += paar[0] + ", "
        stringRechts += paar[1] + ", "
    stringLinks = stringLinks[:-2]
    stringRechts = stringRechts[:-2]
    return detect(stringLinks), detect(stringRechts) 

def maakStamplijst(dico, nReps):
    """
    Maakt een n-voudige stamplijst van het aangegeven woordenboek,
    (of parenlijst) en stuurt deze terug.
    Heeft als bijwerking het argument te husselen als het een parenlijst is.
    """
    if type(dico) is dico: # Als lijst ingevoerd al oké.
        paren = dictList(dico)
    else:
        paren = dico
    stampParen = []
    for k in range(nReps):
        random.shuffle(paren)
        stampParen += paren
    return stampParen

def maakMP3map(paren, naam, van, naar, rust=None):
    """
    Maakt een map met mp3-fragmenten van de paren zoals aangegeven.
    Typischerwijze wordt deze toegepast na maakStampLijst.
    Overschrijft bestaande mappen.
    Foutmeldingen zijn soms te wijten aan fouten in de overzichten.
    Duiken andere fouten op, dan moet er nog goed naar de code gekeken worden.
    Toegestane waarden voor "rust" zijn 1, 2 en 3.
    """
    os.mkdir("mp3-fragmenten\\" + naam)
##    taalLinks, taalRechts = bepaalTalen(paren) # Het paar talen.
    teller = 1
    for paar in paren:
        padLeeg = "mp3-fragmenten\\{}\\{}{}.mp3"
        pad = padLeeg.format(naam, teller, paar[0])
        tts = gTTS(paar[0], lang=van, slow=False)
        tts.save(pad)
        if rust:
            padBron = "pauses\\zzz{}.mp3".format(rust)
            padDoel = "mp3-fragmenten\\{}\\{}zzz.mp3".format(naam, teller)
            copyfile(padBron, padDoel)
        
        teller += 1
        pad = padLeeg.format(naam, teller, paar[1])
        tts = gTTS(paar[1], lang=naar, slow=False)
        tts.save(pad)
        if rust:
            padBron = "pauses\\zzz{}.mp3".format(rust)
            padDoel = "mp3-fragmenten\\{}\\{}zzz.mp3".format(naam, teller)
            copyfile(padBron, padDoel)
        teller += 1

def main(naamOverzicht, van="fr", naar="sp", nReps=3, rust=True, note=""):
    """
    Leest het aangegeven overzicht van woorden,
    schrijft er stamplijsten van en maakt MP3-mappen aan.
    """
    naam = "{}_{}-{}{}reps{}".format(naamOverzicht, van, naar,
                                      nReps, note)
    try:
        rmtree("mp3-fragmenten\\" + naam)
        print("We schrijven een al bestaande MP3-map over.")
    except FileNotFoundError:
        print("Geen mappen met dezelfde naam.")
    try:
        os.remove("txt-stamplijsten\\{}.txt".format(naam))
        print("On écrase un fichier de mots déjà existant/")
    except FileNotFoundError:
        print("Pas de fichier de texte du même nom.")
    paren = leesParenTXT("txt-overzichten\\{}".format(naamOverzicht))
    stampParen = maakStamplijst(paren, nReps)  
    maakMP3map(stampParen, naam, van, naar, rust)
    schrijfParenTXT(stampParen, "txt-stamplijsten\\{}".format(naam))

# ----------------------------------------------------------------

if __name__ == "__main__":
    
    print("Ici nous allons encore faire quelques essais.")

    main("Latijn", van="nl", naar="la", nReps=3, rust=1, note="_nummer6")
    main("Latijn", van="nl", naar="la", nReps=2, rust=1, note="_nummer7")

# TODO: Lezen wat de optatieve parameters doen in de module gTTS.
#       Misschien zitten er nuttige mogelijkheden tussen.
