from .module_ecran import module as ecran
from .module_camera.Camera import Camera
from .module_ecran.Input import Input
from .module_webapp import create_app
import pygame as pg
import io, os, sys
from pathlib import Path
import time
import requests
from dotenv import load_dotenv


class Robot:
    def __init__(self):
        self.load_env_file('.env_to_rename')
        self.webapp = None
        self.debug = True
        self.ecran = None
        self.titre = "Pybot"
        self.actif = True
        self.events = []
        # camera
        self.camera = None
        # Utilisateur connecté
        self.utilisateur_connecte = None

    ### GENERAL - ECRAN ###

    def demarrer_webapp(self):
        '''
            Cette méthode lance de manière non bloquant le serveur web qui s'occupe de la partie base de donnée.
        '''
        self.webapp = create_app(root_dir=os.path.dirname(os.path.abspath(__file__)))
        pid = os.fork()
        if pid:
            self.webapp.run()
            sys.exit()

    def allumer_ecran(self, longueur=800, hauteur=600):
        '''
            Créer un écran avec une longueur et une hauteur de fenêtre passée en argument (en nombre de pixels). \n
            Si un argument n'est pas donné, la longueur par défaut sera 800 pixels et la hauteur par défaut sera 600 pixels.
        '''
        self.ecran = ecran.run(self, longueur, hauteur)
        self.camera = Camera(self.ecran.surface)
        try:
            self.camera.updateUserCardsTracker(self.webapp)
        except ValueError:
            self.message_erreur("L' application web doit être lancé avant d' allumer l'écran.")

    def changer_titre(self, titre):
        '''
            Changer le titre de la fenêtre.
        '''
        try:
            self.ecran.update_title(titre)
        except AttributeError:
            self.message_erreur("Le titre doit être défini aprés création de l'écran.")

    def dessiner_ecran(self):
        '''
            Fonction nécessaire dans une boucle pour mettre à jour l'affichage de l'écran.
        '''
        self.ecran.render()

    def plein_ecran(self, changer):
        '''
            Passer l'ecran en plein ecran (changer=True) ou en sortir (changer=False).
        '''
        self.ecran.update_fullscreen(changer)

    def dort(self, secondes):
        '''
            Le programme restera en attente le nombre de seconde passé en argument.
        '''
        time.sleep(secondes)

    def est_actif(self):
        '''
            Retourne vrai (True) ou faux (False) pour savoir si le robot est toujours actif. \n
            Peut être utilisé pour vérifier la sortie d'une boucle.
        '''
        return self.actif

    def desactiver(self):
        '''
            Passe la variable self.actif du robot avec la valeur False.
        '''
        self.actif = False

    def eteindre_ecran(self):
        '''
            Sert à éteindre correctement l'écran (et la bibliothèque graphique), le robot est inactivé. \n
            Combiné avec un évènement (par exemple appuyer sur une touche ou un bouton) il peut etre utilisé pour arrêter le programme.
        '''
        try:
            self.camera.stop()
            self.ecran.stop()
            self.actif = False
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    ### GENERAL - EVENEMENTS ###

    def ajouter_evenement(self, touche, nom):
        """
            Ajoute à la liste des évènements, un évènement et la touche liée, un évènement peut avoir plusieurs touches. \n
            Voir documentation pour la liste des touches possibles.
        """
        new = (touche.lower(), nom)
        if new not in self.events:
            self.events.append(new)

    def supprimer_evenement(self, nom):
        """
            Supprimer l'évènement donnée en paramètre de la liste des évènements.
        """
        for e in self.events:
            if e[1] == nom:
                self.events.remove(e)

    def verifier_evenements(self):
        """
            Vérifie chaque évènements et retourne un tableau avec les évènements détectés.
        """
        return Input.check(self.events, self)


    ### INTERFACE - BOUTONS ###

    def couleur_fond(self, couleur):
        r"""
            Change la couleur du fond d'écran. \n
            La couleur passée en paramètre doit être au format: (R, G, B). \n
            R, G et B sont des nombres entre 0 et 255.
        """
        try:
            self.ecran.change_background_color(couleur[0], couleur[1], couleur[2])
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    def afficher_fond(self):
        r"""
            Affiche le fond d'écran avec la couleur enregistrée en dernier avec la fonction couleur_fond() \n
            (par défaut, la couleur est noir).
        """
        try:
            self.ecran.draw_background()
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")


    def creer_bouton(self, longueur, hauteur, position_x, position_y, couleur):
        r"""
            Créer et retourner un bouton qui peut être affiché et vérifié plus tard. \n
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du bouton. \n
                * la position x et y du bouton (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du bouton.
        """
        try:
            return self.ecran.create_button(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")


    def dessiner_rectangle(self, longueur, hauteur, position_x, position_y, couleur):
        r"""
            Dessine un rectangle dans la fenêtre. \n
        
            Les paramètres attendus sont : \n
                * la longueur et la hauteur du rectangle. \n
                * la position x et y du rectangle (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la couleur du rectangle.
        """
        try:
            self.ecran.draw_rect(longueur, hauteur, position_x, position_y, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    
    def afficher_texte(self, texte, position_x=0, position_y=0, taille=16, couleur=(0, 0, 0)):
        r"""
            Affiche un texte dans la fenêtre. \n

            Les paramètres attendus sont : \n
                * le texte à afficher. \n
                * la position x et y du texte (son coin en haut à gauche) par rapport à la fenêtre. \n
                * la taille du texte. \n
                * la couleur du texte.
        """

        try:

            self.ecran.draw_text(texte, position_x, position_y, taille, couleur)
        except AttributeError:
            self.message_erreur("L'écran n'a pas été allumé.")

    ### CAMERA - PHOTOS ###
    
    def afficher_camera(self, position_x=0, position_y=0):
        """
            Affiche la caméra aux coordonées x et y.
        self.ecran.display_camera(x, y)
        """
        self.camera.display(position_x, position_y)

    def prendre_photo(self, nom_fichier):
        """
            Capture une image de la caméra au nom du fichier passé en paramètre et l'enregistre dans le dossier images.
        """
        self.camera.capture(nom_fichier)

    def afficher_image(self, chemin_fichier, position_x, position_y):
        r"""
            Afficher une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Les coordonnées x et y ou seront affiché l'image.
        """
        print("afficher_image_from_path:", type())
        self.ecran.display_image_from_path(chemin_fichier, position_x, position_y)

    def appliquer_filtre(self, chemin_fichier, nom_filtre):
        r"""
            Applique un filtre sur une image. \n
            Les paramètres attendus sont : \n
                * Le chemin et nom du fichier. (ex: /images/photo.jpg) \n
                * Le nom du filtre. (ex: cartoon, alien, tourner...) \n
        (voir documentation pour la liste complète des filtres: https://42angouleme.github.io/ref/)
        """
        self.ecran.set_filter(chemin_fichier, nom_filtre)

    ### RECONNAISANCE CARTES - SESSION UTILISATEUR ###

    def connecter(self, seuil_minimal=0.75, seuil_arret_recherche=0.85):
        """{
                        'first_name': ''
                        }
            Affiche à l' écran un cadre autour de la carte et
            connecte l'utilisateur si reconnu.

            Paramètres:
                * seuil_minimal (défaut: 0.75) : score minimum pour
                    qu' une carte détectée soit considérée comme valide.
                * seuil_arret_recherche (défaut: 0.85) : score pour
                    qu' une carte détectée soit interprétée comme la bonne.
        """
        if self.webapp is None:
            self.message_avertissement(
                "La fonction Robot.connecter() a été appelée"
                "sans Robot.demarrer_webapp()")
            return ""
        elif not self.camera.camera.isOpened():
            return
        utilisateur_reconnu, _ = self.camera.detect_user(seuil_minimal,
                                                         seuil_arret_recherche)
        if utilisateur_reconnu and self.verifier_session():
            self.message_avertissement("Un utilisateur est déjà connecté.")
        elif utilisateur_reconnu:
            self.utilisateur_connecte = utilisateur_reconnu

    def detecter_carte(self, seuil_minimal=0.75, seuil_arret_recherche=0.85):
        if self.webapp is None:
            self.message_avertissement(
                "La fonction Robot.detecter_carte() a été appelée"
                "sans Robot.demarrer_webapp()")
            return ""
        elif not self.camera.camera.isOpened():
            return
        carte_reconnue, _ = self.camera.detect_card(seuil_minimal,
                                                    seuil_arret_recherche)
        return carte_reconnue

    def afficher_carte_detectee(self, carte_detectee, position_x, position_y):
        r"""
            Afficher la carte détectée. \n
            Les paramètres attendus sont : \n
                * L' image de la carte detectée par Robot.detecter_carte() \n
                * Les coordonnées x et y ou seront affiché l'image.
        """
        self.ecran.display_image(carte_detectee, position_x, position_y)

    def deconnecter(self):
        """
            Déconnecte la personne actuellement connectée.
        """
        self.utilisateur_connecte = None

    def verifier_session(self):
        """
            Indique si un utilisateur est déjà connecté.

            Retourne:
                * True: Si une personne est connectée
                * False: Sinon
        """
        return self.utilisateur_connecte is not None

    def creer_utilisateur(self, prenom: str, nom: str, carte):
        """
            Créer un utilisateur avec les données renseignées en paramètres

        Paramètres:
            - prenom: son prénom
            - nom: son nom de famille
            - carte: l' image de sa carte ( générée avec Robot.detecter_carte())
        """
        if self.verifier_session():
            self.message_avertissement("Un utilisateur est déjà connecté")
            return
        elif carte is None:
            self.message_avertissement(
                "Creation d'Utilisateur avec une carte invalide (=None)"
            )
            return
        pg.image.save(carte, ".tmp_card.png")
        with open(".tmp_card.png", "rb") as img:
            files = {
                "picture": ("picture.png", img, "image/png"),
            }
            new_user = {
                "first_name": prenom,
                "last_name": nom,
            }
            os.unlink(".tmp_card.png")
            try:
                response = requests.post(
                    f"{APP_BASE_URL}/api/users", data=new_user, files=files
                )
                if response.status_code != 201:
                    self.message_erreur("[HTTP ERROR]" + str(response.content))
                else:
                    print("Success")
                    # Update les cartes des sessions chargées lors
                    #   de la construction de CardsTracker
                    self.camera.updateUserCardsTracker(self.webapp)
            except Exception as e:
                self.message_erreur("[HTTP EXCEPTION]" + str(e))

    def supprimer_utilisateur(self):
        """
           Supprime l' utilisateur connecté.
        """
        if not self.verifier_session():
            self.message_avertissement("Aucun utilisateur n' est connecté")
            return
        try:
            id = self.utilisateur_connecte.id
            response = requests.delete(f"{APP_BASE_URL}/api/users/{id}")
            if response.status_code != 200:
                self.message_erreur("[HTTP ERROR]" + str(response.content))
            else:
                self.deconnecter()
                # Update les cartes des sessions chargées lors
                #   de la construction de CardsTracker
                self.camera.updateUserCardsTracker(self.webapp)
        except Exception as e:
            self.message_erreur("[HTTP EXCEPTION]" + str(e))

    ### IA ###

    def entrainer(self, texte):
        """
            ...
        """
        print("entrainer avec", texte)

    def repondre_question(self, texte):
        """
            ...
        """
        print("envoyer question")
        return "Réponse"

    def choisir_emotion(texte, liste_emotions):
        """
            ...
        """
        print("avec", texte, "choisir emotion dans", liste_emotions)

    ### AUDIO ###

    def parler(self, texte):
        """
            ...
        """
        print("texte conversion audio", texte)

    ### MICROPHONE ###

    def enregister_audio(self):
        """
            ...
        """
        print("enregistrer audio")

    ### AUTRES ###
    def message_erreur(self, msg):
        print(f"\033[91mErreur: {msg}\033[00m", file=sys.stderr)

    def message_avertissement(self, msg):
        print(f"\033[33mAttention: {msg}\033[00m", file=sys.stderr)

    APP_BASE_URL, APP_ADRESS, APP_PORT = [""] * 3
    @staticmethod
    def load_env_file(path_file: str = '.env'):
        global APP_BASE_URL, APP_ADRESS, APP_PORT
        load_dotenv(dotenv_path=Path(path_file))
        APP_BASE_URL = os.getenv('WEBAPP_BASE_URI')
        APP_ADRESS = APP_BASE_URL.split(':')[1][2:]
        APP_PORT = APP_BASE_URL.split(':')[2]
