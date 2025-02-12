from pybot import Robot, Couleur

# ---- Dans main_initialisation.py -------
robot = Robot()
robot.demarrer_webapp()
long = 840
haut = 300
robot.attributs.mettre_a_jour_affichage = True
robot.attributs.zone = "menu"
robot.attributs.paroles_index = 0

robot.attributs.paroles = [
    "Salut ! Je m'appelle Pybot le robot. Je suis ici pour t'aider,",
    "jouer avec toi et répondre à toutes tes questions.",
    "Je peux raconter des histoires passionnantes, jouer à des jeux amusants,",
    "et même t'aider avec tes devoirs.",
    "Alors, prêt pour des moments incroyables en ma compagnie ?"
]

def initialisation_fenetre():
    robot.creer_fenetre(long, haut)
    robot.changer_titre("Bonjour boutons!")
    robot.couleur_fond(Couleur.ROSE)


def initialisation_boutons():
    boutons = robot.attributs.boutons
    boutons.menu = robot.creer_bouton(120, 50, 10, 10, Couleur.CYAN)
    boutons.menu.ajouter_texte("Menu", couleur=Couleur.VIOLET)
    boutons.quitter = robot.creer_bouton(120, 50, 10, 110, Couleur.VERT)
    boutons.quitter.ajouter_texte("Quitter", 10, 10, 24)
    boutons.discussion = robot.creer_bouton(120, 50, 10, 220, Couleur.JAUNE)
    boutons.discussion.ajouter_texte("Discussion", 5, 30, 20, Couleur.MAGENTA)
    boutons.plus = robot.creer_bouton(180, 40, 200, 200, Couleur.ROSE)
    boutons.plus.ajouter_texte("suite du texte", 10, 10, 20, Couleur.NOIR)

def initialisation_evenements():
    robot.ajouter_evenement("echap", "stop")
# ----------------------------------------


# -------- Dans main_boucle.py -----------
def boucle_boutons():
    boutons = robot.attributs.boutons
    if boutons.menu.est_actif():
        robot.attributs.zone = "menu"
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.quitter.est_actif():
        robot.fermer_fenetre()
    if boutons.discussion.est_actif():
        robot.attributs.zone = "discussion"
        robot.attributs.mettre_a_jour_affichage = True
    if boutons.plus.est_actif():
        robot.attributs.paroles_index = robot.attributs.paroles_index + 1
        if robot.attributs.paroles_index == len(robot.attributs.paroles):
            robot.attributs.paroles_index = 0
        robot.attributs.mettre_a_jour_affichage = True

def boucle_evenements():
    evenements = robot.verifier_evenements()
    if "stop" in evenements:
        robot.fermer_fenetre()

def boucle_fenetre():
    zone = robot.attributs.zone
    boutons = robot.attributs.boutons
    mettre_a_jour_affichage = robot.attributs.mettre_a_jour_affichage
    if mettre_a_jour_affichage:
        if zone == "menu":
            robot.couleur_fond(Couleur.ROUGE)
        else:
            robot.couleur_fond(Couleur.BLEU)
        robot.afficher_fond()
        boutons.menu.afficher()
        boutons.quitter.afficher()
        if zone == "menu":
            boutons.discussion.afficher()
        if zone == "discussion":
            index = robot.attributs.paroles_index
            robot.dessiner_rectangle(685, 40, 150, 70, Couleur.BLANC)
            robot.afficher_texte(robot.attributs.paroles[index], 150, 80, 20)
            boutons.plus.afficher()
        robot.attributs.mettre_a_jour_affichage = False
# ----------------------------------------


if __name__ == "__main__":
    initialisation_fenetre()
    initialisation_evenements()
    initialisation_boutons()
    while robot.est_actif():
        boucle_evenements()
        boucle_boutons()
        boucle_fenetre()
        robot.actualiser_affichage()
