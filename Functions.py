import random
from word_class import Word

""" Toutes les fonctions qu'on est susceptibles d'appeler pour le traitement, sont déportées dans ce fichier
pour plus de clarté. Certaines sont utilisées, certaines servent juste à des tests"""

listOfWordsObjects = [Word]  #  Liste de mots créés à partir de l'objet "Word", défini dans word_class.
""" Finalement, je n'utilise pas ces objets Word, car l'apprentissage est extrêmement long. Le but était de créer une 
liste de tous les mots possibles, avec leurs carateristiques, les mots suivants possibles, etc...
Ca serait la bonne méthode si on utilisait le même modèle d'apprentissage très souvent. L'apprentissage serait 
super long, (des dizaines d'heures), mais ensuite la génération de texte serait plus rapide."""


# Prend en paramètre le texte source, et renvoit la liste de tous les mots premiers, c'est à dire
# tous les mots qui peuvent être utilisés pour débuter une phrase"""
def findFirstWords(myText: str):
    listOfFirstWords = []
    for sentence in myText.split(". "):
        if len(sentence) > 0:
            listOfFirstWords.append(sentence.split()[0])
    print("taille de liste: " + str(len(listOfFirstWords)))
    return listOfFirstWords


# Même chose si on utilisait l'objet "Word"
def firstWordsObjects(myText: str):

    for sentence in myText.split(". "):
        if len(sentence) > 0:
            mWordName = sentence.split()[0]
            print(mWordName)
            followings = getAllFollowingWordForWord(mWordName)
            mWord = Word(sentence.split()[0], followings, True, False)
            listOfWordsObjects.append(mWord)


# Récupération de tous les mots en objet "Word"
def allWordsObjects(myText: str):
    listDots = [".", "?", "!", ";", ":"]
    for word in myText.split():
        mWord = Word
        followings = getAllFollowingWordForWord(word)
        if word[len(word)] in listDots:
            print(mWord)
            mWord = Word(word, followings, False, True)
        else:
            print(mWord)
            mWord = Word(word, followings, False, False)
        listOfWordsObjects.append(mWord)


# Prend en paramètre le texte source, renvoit la liste de tous les mots
def findAllWords(myText: str):
    listOfAllWords = []
    for word in myText.split():
        if word not in listOfAllWords:
            listOfAllWords.append(word)
    return listOfAllWords


# Renvoit les indexs de tous les endroits où un mot donné est trouvé dans le texte
def getAllIndexesForWord(myText: str, word: str):
    start = 0
    while word in myText[start:len(myText)]:
        index = myText.index(word, start, len(myText))
        start = index + len(word)
        print(index)


# Renvoit tous les mots qui peuvent suivre un mot donné
def getAllFollowingWordForWord(myText: str, word: str):
    allFollowings = []
    word = word + " "
    start = 0
    while word in myText[start:len(myText)]:
        index = myText.index(word, start, len(myText))
        start = index + len(word)
        if len(myText[start:len(myText)].split()) > 0:
            followingFound = myText[start:len(myText)].split()[0]
            allFollowings.append(followingFound)
    return allFollowings


# Renvoit tous les blocs de 2 mots qui peuvent suivre un mot donné
def getAll2FollowingWordForWord(myText: str, word: str):
    allFollowings = []
    word = word + " "
    start = 0
    while word in myText[start:len(myText)]:
        index = myText.index(word, start, len(myText))
        start = index + len(word)
        if len(myText[start:len(myText)].split()) > 1:
            followingFound = myText[start:len(myText)].split()[0] + " " + myText[start:len(myText)].split()[1]
            allFollowings.append(followingFound)
    return allFollowings


# Renvoit tous les blocs de 3 mots qui peuvent suivre un mot donné
def getAll3FollowingWordForWord(myText: str, word: str):
    allFollowings = []
    word = word + " "
    start = 0
    while word in myText[start:len(myText)]:
        index = myText.index(word, start, len(myText))
        start = index + len(word)
        if len(myText[start:len(myText)].split()) > 2:
            followingFound = myText[start:len(myText)].split()[0] \
                             + " " + myText[start:len(myText)].split()[1] \
                             + " " + myText[start:len(myText)].split()[2]
            allFollowings.append(followingFound)
    return allFollowings


# Renvoit le nombre de fois qu'un mot est trouvé dans le texte
def getNumberOfOccurencesForWord(myText: str, word: str):
    start = 0
    occurences = 0
    while word in myText[start:len(myText)]:
        index = myText.index(word, start, len(myText))
        start = index + len(word)
        occurences += 1
    return occurences


# Renvoit un dictionnaire de tous les mots avec leur fréquence d'apparition
def createDictionnaryOfWordsWithOccurences():
    thisDict = {str: int}
    list0fAllWords = findAllWords('')

    for word in list0fAllWords:
        number = getNumberOfOccurencesForWord(word)
        thisDict[word] = number

    print(thisDict)


# Renvoit un dictionnaire de tous les mots avec les mots qui peuvent venir après
def createDictionnaryOfWordsWithAllFollowings():
    thisDict = {str: [str]}
    list0fAllWords = findAllWords()

    for word in list0fAllWords:
        followings = getAllFollowingWordForWord(word)
        thisDict[word] = followings

    print(thisDict["the"])


# Renvoit aléatoirement un mot premier (et j'élimine ceux qui commencent par un chiffre, c'est moche!)
def pickUpOneFirstWord(listOfFirstWords: [str]):
    firstWord = "1"
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    while firstWord[0] in numbers:
        rand = random.randrange(len(listOfFirstWords))
        firstWord = listOfFirstWords[rand]

    return firstWord


# Test de génération d'un texte pour valider certaines fonctions
def writeText(words: int):
    i = 0
    lastWord = pickUpOneFirstWord()
    print(lastWord)

    while i < 100:
        followings = getAllFollowingWordForWord(lastWord)
        if len(followings) == 1:
            lastWord = pickUpOneFirstWord()
        else:
            rand = random.randrange(1, len(followings))
            lastWord = followings[rand]
        print(lastWord)
        i += 1


# Fonction pour supprimer tout un tas de caractères chelou qui pourissent le texte
def cleanWeirdos(word: str):
    word = word.replace("*", "")
    word = word.replace("#", "")
    word = word.replace("[", "")
    word = word.replace("]", "")
    word = word.replace("`", "")
    word = word.replace("\"", "")
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("»", "")
    word = word.replace("«", "")

    return word
