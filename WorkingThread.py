from PyQt5 import QtCore
import threading
from Functions import *

""" Thread qui assure le traitement des données """


class WorkingThread(QtCore.QThread):  # Thread de type QThread pour pouvoir communiquer avec l'interface PyQt
    signal = QtCore.pyqtSignal(object)  # Le signal qui est envoyé à l'UI pour mise à jour
    source: str                 # texte source
    listOfFirstWords: [str]     # liste des mots premiers
    listFollowings: [str]       # liste des mots suivants
    lastWord: str               # dernier mot utilisé

    sourceFilePath: str         # chemin du fichier source +
    taille_sortie: int          # tous les
    taille_paragraphe: int      # paramètres demandés
    taille_blocs: int           # etc...

    nbr_mots_sortie = 0         # nombre de mots de la sortie en cours
    nbr_mots_paragraphe = 0     # nombre de mots du paragraphe en cours
    listEndings = [".", "?", "!", ";", ":"]  # liste des caractères qui définissent la fin d'une phrase

    def __init__(self, path: str, taille_sortie: int, taille_paragraphe: int, taille_blocs: int):
        # Constructeur de la classe avec les paramètres passés par l'UI
        QtCore.QThread.__init__(self)
        self._stop = threading.Event()
        self.sourceFilePath = path
        self.taille_sortie = taille_sortie
        self.taille_paragraphe = taille_paragraphe
        self.taille_blocs = taille_blocs

    def run(self):  # traitement du thread
        self.loadSourceStr()        # on charge le fichier source
        self.getFirstWords()        # on recupère les mots premiers
        while self.nbr_mots_sortie < self.taille_sortie:  # tant qu'on n'a pas atteint le nombre de mots demandés...
            self.make_sentence()  # On fait une nouvelle phrase
            self.sendToGUI("addOutput", " ")  # et on envoit un espace à l'UI
            if self.nbr_mots_paragraphe > self.taille_paragraphe:  # Si la taille d'un paragraphe est atteinte
                self.nbr_mots_paragraphe = 0  # on remet le compteur paragraphe à zéro
                self.sendToGUI("addOutput", "\n\n   ")  # et on envoit à l'UI 2 retours a la ligne et des espaces
        self._stop.set()  # a la fin on stoppe le thread

    def loadSourceStr(self):
        File_object = open(self.sourceFilePath)
        self.source = cleanWeirdos(File_object.read())

    def make_sentence(self):  # pour faire une phrase
        self.pickOneFirstWord()  # on la commence par un mot premier
        while True:  # puis on lui ajoute des mots suivants jusqu'à ce que l'on trouve un caractère de fin de phrase.
            self.getFollowings()
            if self.lastWord[len(self.lastWord)-1] in self.listEndings:
                return

    def getFirstWords(self):  # récuperation des mots premiers et envoi à l'UI
        self.sendToGUI("clearFirstWords", "none")
        self.listOfFirstWords = findFirstWords(self.source)
        self.sendToGUI("addFirstWord", self.listOfFirstWords)

    def pickOneFirstWord(self):  # choix aléatoire d'un mot premier et envoi à l'UI
        mWord = pickUpOneFirstWord(self.listOfFirstWords)
        self.lastWord = mWord
        self.sendToGUI("addOutput", mWord)
        self.nbr_mots_sortie += self.taille_blocs
        self.nbr_mots_paragraphe += self.taille_blocs
        self.sendToGUI("updateProgress", self.nbr_mots_sortie/self.taille_sortie)

    def getFollowings(self):  # appel de la fonction de récupération des mots suivants
        # selon le nombre de blocs de mots demandés
        if self.taille_blocs == 1:
            self.listFollowings = getAllFollowingWordForWord(self.source, self.lastWord)
        if self.taille_blocs == 2:
            self.listFollowings = getAll2FollowingWordForWord(self.source, self.lastWord)
        if self.taille_blocs == 3:
            self.listFollowings = getAll3FollowingWordForWord(self.source, self.lastWord)

        self.sendToGUI("addFollowings", self.listFollowings)
        mWord = self.listFollowings[random.randrange(len(self.listFollowings))] if len(self.listFollowings) > 0 else "."
        self.lastWord = (mWord.split()[len(mWord.split()) - 1])
        self.sendToGUI("addOutput", mWord)
        self.nbr_mots_sortie += self.taille_blocs
        self.nbr_mots_paragraphe += self.taille_blocs
        self.sendToGUI("updateProgress", self.nbr_mots_sortie / self.taille_sortie)

    # Fonction qui envoit le signal à l'UI
    def sendToGUI(self, command: str, data):
        self.signal.emit((command, data))


