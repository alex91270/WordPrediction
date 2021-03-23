from PyQt5.QtWidgets import QFileDialog
import WorkingThread
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WorkingThread import WorkingThread

"""Classe hébergeant l'interface utilisateur. Point d'entrée du programme."""


class Window(QtWidgets.QMainWindow):
    sourceFilePath = str  #chemin du fichier source
    workingThread = WorkingThread  #Déclaration du thread qui fera le travail
    sortie = ""  #string contenant le texte final qui sera généré
    fileSelected = False  #boolean qui vérifie qu'un fichier source a bien été selectionné

    def __init__(self):
        #  constructeur de la classe
        super(Window, self).__init__()
        self.setGeometry(0, 0, 1923, 1000)
        self.setWindowTitle("Prediction de texte")
        # dictionnaire associant les valeurs du comboBox avec les valeurs correspondantes de type Integer
        markovOptions = {"1 mot": 1, "2 mots": 2, "3 mots": 3}
        self.showMaximized()

        """Fonction appelée quand on appuie sur le bouton parcourir"""
        def bouton_parcourir_pushed():
            self.sourceFilePath = ""
            filedialog = QFileDialog(self)  #FileDialog pour chercher le fichier
            filedialog.setDefaultSuffix("txt")
            filedialog.setNameFilter("Fichiers texte (*.txt)")
            selected = filedialog.exec()
            if selected:  #Si fichier selectionné
                self.fileSelected = True
                self.sourceFilePath = filedialog.selectedFiles()[0]
                filename = self.sourceFilePath
                # formatage du chemin s'il est trop long, pour que visuellement, il rentre dans le champ texte:
                if len(self.sourceFilePath) > 35:
                    filename = "..." + self.sourceFilePath[len(self.sourceFilePath) - 35: len(self.sourceFilePath)]
                self.textEdit_source.setText(filename)
            else:
                return
            if self.sourceFilePath == "":
                return

        """Fonction appelée quand on appuie sur le bouton GO"""
        def bouton_GO_pushed():
            self.pushButton_GO.setEnabled(False)
            # Verification de la présence de tous les paramètres requis. Sinon, message d'erreur.
            if self.fileSelected is False or self.textEdit_nbr_mots.text() == "" or self.textEdit_paragraphe.text() == "":
                error_dialog = QtWidgets.QErrorMessage()
                error_dialog.showMessage('Il manque des paramètres!')
                error_dialog.exec_()
                return
            self.sortie = ""
            self.progressBar.setValue(0)  # Mise à zéro de la progressBar
            self.textEdit_sortie.clear()  # Vidage de tous les champs texte et listes
            self.textEdit_mot_en_cours.clear()
            self.listView_mots_premiers.clear()
            self.listWidget_mots_suivants.clear()
            #  Instanciation de la classe de travail en passant les paramètres
            self.workingThread = WorkingThread(str(self.sourceFilePath), int(self.textEdit_nbr_mots.text()),
                                               int(self.textEdit_paragraphe.text()),
                                               markovOptions[self.comboBox.currentText()])
            #  Mise en place d'un "callback": On indique qu'il faudra déclencher le fonction "on_data_ready"
            #  à chaque fois que le "signal" est reçu du thread secondaire.
            self.workingThread.signal.connect(on_data_ready)
            self.workingThread.start()

        # Déclaration des éléments visuels de l'UI:
        self.onlyInt = QIntValidator()
        self.frame_parametres = QtWidgets.QGroupBox(self)
        self.frame_parametres.setTitle("Paramètres requis")
        self.frame_parametres.setGeometry(QtCore.QRect(390, 10, 1521, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_parametres.setFont(font)
        self.frame_parametres.setObjectName("frame_parametres")
        self.frame_parametres.show()

        self.label_source = QtWidgets.QLabel("Fichier source", self.frame_parametres)
        self.label_source.setGeometry(QtCore.QRect(150, 40, 121, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_source.setFont(font)
        self.label_source.setObjectName("label_source")
        self.label_source.show()

        self.label_nbr_mots = QtWidgets.QLabel("Nombre de mots souhaité", self.frame_parametres)
        self.label_nbr_mots.setGeometry(QtCore.QRect(540, 40, 250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_nbr_mots.setFont(font)
        self.label_nbr_mots.setObjectName("label_nbr_mots")
        self.label_nbr_mots.show()

        self.label_paragraphe = QtWidgets.QLabel("Nombre de mots par paragraphe", self.frame_parametres)
        self.label_paragraphe.setGeometry(QtCore.QRect(810, 40, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_paragraphe.setFont(font)
        self.label_paragraphe.setObjectName("label_paragraphe")
        self.label_paragraphe.show()

        self.label_taille_blocs = QtWidgets.QLabel("Taille des blocs de mots", self.frame_parametres)
        self.label_taille_blocs.setGeometry(QtCore.QRect(1140, 40, 220, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_taille_blocs.setFont(font)
        self.label_taille_blocs.setObjectName("label_taille_blocs")
        self.label_taille_blocs.show()

        self.textEdit_source = QtWidgets.QTextEdit(self.frame_parametres)
        self.textEdit_source.setGeometry(QtCore.QRect(10, 70, 391, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_source.setFont(font)
        self.textEdit_source.setObjectName("textEdit_source")
        self.textEdit_source.show()

        self.comboBox = QtWidgets.QComboBox(self.frame_parametres)
        self.comboBox.setGeometry(QtCore.QRect(1190, 70, 121, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(markovOptions.keys())
        self.comboBox.show()

        self.textEdit_paragraphe = QtWidgets.QLineEdit(self.frame_parametres)
        self.textEdit_paragraphe.setGeometry(QtCore.QRect(910, 70, 71, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_paragraphe.setFont(font)
        self.textEdit_paragraphe.setObjectName("textEdit_paragraphe")
        self.textEdit_paragraphe.setValidator(self.onlyInt)
        self.textEdit_paragraphe.show()

        self.textEdit_nbr_mots = QtWidgets.QLineEdit(self.frame_parametres)
        self.textEdit_nbr_mots.setGeometry(QtCore.QRect(620, 70, 81, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_nbr_mots.setFont(font)
        self.textEdit_nbr_mots.setObjectName("textEdit_nbr_mots")
        self.textEdit_nbr_mots.setValidator(self.onlyInt)
        self.textEdit_nbr_mots.show()

        self.pushButton_parcourir = QtWidgets.QPushButton("Parcourir", self.frame_parametres)
        self.pushButton_parcourir.setGeometry(QtCore.QRect(410, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_parcourir.setFont(font)
        self.pushButton_parcourir.setAutoRepeatDelay(297)
        self.pushButton_parcourir.setObjectName("pushButton_parcourir")
        self.pushButton_parcourir.clicked.connect(bouton_parcourir_pushed)
        self.pushButton_parcourir.show()

        self.pushButton_GO = QtWidgets.QPushButton(self.frame_parametres)
        self.pushButton_GO.setGeometry(QtCore.QRect(1410, 20, 91, 91))
        self.pushButton_GO.setIcon(QIcon(QPixmap(os.getcwd() + "/assets/go.png")))
        self.pushButton_GO.setIconSize(QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_GO.setFont(font)
        self.pushButton_GO.setText("")
        self.pushButton_GO.setObjectName("pushButton_GO")
        self.pushButton_GO.clicked.connect(bouton_GO_pushed)
        self.pushButton_GO.show()

        self.frame_traitement = QtWidgets.QFrame(self)
        self.frame_traitement.setGeometry(QtCore.QRect(10, 10, 371, 961))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_traitement.setFont(font)
        self.frame_traitement.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_traitement.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_traitement.setLineWidth(3)
        self.frame_traitement.setObjectName("frame_traitement")
        self.frame_traitement.show()

        self.label_mots_premiers = QtWidgets.QLabel("Mots de début de phrases", self.frame_traitement)
        self.label_mots_premiers.setEnabled(True)
        self.label_mots_premiers.setGeometry(QtCore.QRect(10, 10, 260, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_mots_premiers.setFont(font)
        self.label_mots_premiers.setObjectName("label_mots_premiers")
        self.label_mots_premiers.show()

        self.label_mot_en_cours = QtWidgets.QLabel("Dernier mot utilisé", self.frame_traitement)
        self.label_mot_en_cours.setGeometry(QtCore.QRect(10, 380, 200, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_mot_en_cours.setFont(font)
        self.label_mot_en_cours.setObjectName("label_mot_en_cours")
        self.label_mot_en_cours.show()

        self.label_mots_suivants = QtWidgets.QLabel("Mots suivants possibles", self.frame_traitement)
        self.label_mots_suivants.setGeometry(QtCore.QRect(10, 450, 260, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_mots_suivants.setFont(font)
        self.label_mots_suivants.setObjectName("label_mots_suivants")
        self.label_mots_suivants.show()

        self.textEdit_mot_en_cours = QtWidgets.QTextEdit(self.frame_traitement)
        self.textEdit_mot_en_cours.setGeometry(QtCore.QRect(10, 400, 351, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_mot_en_cours.setFont(font)
        self.textEdit_mot_en_cours.setObjectName("textEdit_mot_en_cours")
        self.textEdit_mot_en_cours.show()

        self.listView_mots_premiers = QtWidgets.QListWidget(self.frame_traitement)
        self.listView_mots_premiers.setGeometry(QtCore.QRect(10, 30, 351, 331))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listView_mots_premiers.setFont(font)
        self.listView_mots_premiers.setObjectName("listView_mots_premiers")
        self.listView_mots_premiers.show()

        self.listWidget_mots_suivants = QtWidgets.QListWidget(self.frame_traitement)
        self.listWidget_mots_suivants.setGeometry(QtCore.QRect(10, 475, 351, 471))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidget_mots_suivants.setFont(font)
        self.listWidget_mots_suivants.setObjectName("listWidget_mots_suivants")
        self.listWidget_mots_suivants.show()

        self.frame_sortie = QtWidgets.QFrame(self)
        self.frame_sortie.setGeometry(QtCore.QRect(390, 140, 1521, 831))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_sortie.setFont(font)
        self.frame_sortie.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_sortie.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sortie.setLineWidth(3)
        self.frame_sortie.setObjectName("frame_sortie")
        self.frame_sortie.show()

        self.progressBar = QtWidgets.QProgressBar(self.frame_sortie)
        self.progressBar.setGeometry(QtCore.QRect(10, 782, 1491, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.show()

        self.textEdit_sortie = QtWidgets.QTextEdit(self.frame_sortie)
        self.textEdit_sortie.setGeometry(QtCore.QRect(20, 20, 1481, 741))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_sortie.setFont(font)
        self.textEdit_sortie.setObjectName("textEdit_sortie")
        self.textEdit_sortie.show()
        self.progressBar.setValue(0)

        self.textEdit_nbr_mots.setText("100")
        self.textEdit_paragraphe.setText("10")
        self.listWidget_mots_suivants.setEnabled(False)
        self.listView_mots_premiers.setEnabled(False)
        self.textEdit_mot_en_cours.setEnabled(False)

        # Callback déclenché à la reception du signal. Le thread de travail envoit un "tuple". Un couple de 2 valeurs:
        # - La première valeur (data[0]) est un string décrivant l'action requise
        # - La deuxième valeur (data[1]) contient les données à traiter
        def on_data_ready(data):
            if data[0] == "clearFirstWords":  # Effacement de la liste des mots premiers
                self.listView_mots_premiers.clear()
            if data[0] == "addFirstWord":  # Remplissage de la liste des mots premiers
                i = 1
                while i < len(data[1]):
                    self.listView_mots_premiers.addItem(data[1][i])
                    i += 1
            if data[0] == "addFollowings":  # Remplissage de la liste desw mots suivants
                self.listWidget_mots_suivants.clear()
                i = 1
                while i < len(data[1]):
                    self.listWidget_mots_suivants.addItem(data[1][i])
                    i += 1
            if data[0] == "addOutput":  # Ajout de mots au champ de sortie
                self.sortie = self.sortie + data[1] + " "
                self.textEdit_sortie.setText(self.sortie)
                lastWord = data[1].split()[len(data[1].split()) - 1] if len(data[1].split()) > 0 else " "
                self.textEdit_mot_en_cours.setText(lastWord)
            if data[0] == "updateProgress":  # Mise à jour de la progressBar
                if data[1] > 1:
                    self.progressBar.setValue(100)
                else:
                    self.progressBar.setValue(data[1]*100)
            if data[0] == "end":
                self.pushButton_GO.setEnabled(True)


# Instructions obligatoires pour lancer le thread principal (thread de l'UI)
app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())

