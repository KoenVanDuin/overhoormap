"""EEn code waar ik gewoon maar wat hb uitgeprobeerd."""
import os
from gtts import gTTS

# TODO: Essayer ce truc:
def saveProbeer(extrait, nom):
    """
    Probeert een fragment met de gegeven naam op te slaan,
    en doet dit niet als er al een met die naam bestaat.
    """
    try:
        mapnaam = "mp3-fragmenten\\"
        extrait.save("{}".format(nom))
        print("Nou moe, het lijkt wel te lukken.")
    except PermissionError:
        mot = "Il y a déja un son du nom de {}."
        print(mot.format(nom))
        print("Pourquoi je ne vois rien, bordel?")

def saveForceer(extrait,nom):
    """TODO: écrire une chaîne de doc."""
    pass
    # TODO: écrire le corps un peu comme dans le cas ci-dessus.
    

tts = gTTS("Un chagrin partagé diminue de moitié.", lang="fr")

tekst = "Alea iacta est. Veni vidi vici."
tekst+= " Quid licet Iovi, licet non bovi."
tekst+= " Mens sana in corpore sano."
tekst+= " Arbores non ambulare possunt."
tts2 = gTTS(tekst, lang="la", slow=True)

print("Wat nu gebeurt zou moeten mislukken")
saveProbeer(tts2, "LatijnTest")

# TODO: De langzame optie proberen.


print("fin de nos essais.")

# Pour le cas où il y a déjà un son portant le nom prévu.
# TODO: écrire une fonction qui enregistre un son en écrasant.
# TODO: écrire une fonction qui tente d'enregistrer et qui laisse tomber.

# TODO: De overgang txt-overzichten => stamplijsten.
# TODO: De overgang stamplijsten => mp3-fragmenten.

# TODO: Ensuite regarder sous quelle forme on peut récupérer des mots,
#       regarder quelle serait la meilleure façon de les enregistrer.
#       (Des fichiers .txt ou autrement?)

# TODO: Lezen wat de optatieve parameters doen in de module.
#       Misschien zitten er nuttige mogelijkheden tussen.


# Peut-être regarder par ici:

