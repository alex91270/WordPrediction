"""Objet Word"""


class Word:

    name: str  # son nom
    following_words: [str]  #Liste de tous les mots qui peuvent le suivre
    is_first: bool  # dit si c'est un mot premier
    is_last: bool  # dit si c'est un mot de fin de phrase

    def __init__(self, name, following, first, last):
        self.name = name
        self.following_words = following
        self.is_first = first
        self.is_last = last

    def isFirst(self):
        return self.is_first

    def isLast(self):
        return self.is_last

    def getFollowings(self):
        return self.following_words


