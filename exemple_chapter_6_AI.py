from pybot import Robot
robot = Robot()

long = 1200
haut = 1000

blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (235, 64, 52)
rouge_sombre = (117, 23, 16)
bleu = (52, 164, 235)
bleu_sombre = (30, 93, 133)
vert = (105, 230, 83)
vert_sombre = (59, 135, 46)
jaune = (237, 212, 66)
jaune_sombre = (171, 128, 19)

bouton_question = None
bouton_stop = None
text_area = None
text_area_bis = None

discussion_commencer = False

mettre_a_jour_affichage = True

def preparer_programme():
    global bouton_question, bouton_stop, text_area, text_area_bis
    robot.creer_fenetre(long, haut)
    robot.changer_titre("Bonjour Robot!")
    robot.couleur_fond(noir)
    robot.ajouter_evenement("echap", "stop")
    bouton_question = robot.creer_bouton(200, 60, 10, 10, bleu)
    bouton_question.ajouter_texte("Poser question", 5, 20)
    bouton_stop = robot.creer_bouton(200, 60, 10, 900, vert)
    bouton_stop.ajouter_texte("Quitter", 10, 10, 20)
    text_area = robot.creer_zone_texte(600, 100, 300, 250, blanc)
    text_area_bis = robot.creer_zone_texte(600, 100, 300, 400, blanc)
    text_area.modifier_couleur_police(vert)
    robot.ajouter_evenement("C", "C")

def dessiner_fenetre():  
    global mettre_a_jour_affichage, discussion_commencer, text_area, text_area_bis
    if mettre_a_jour_affichage:
        robot.afficher_fond()
        bouton_question.afficher()
        bouton_stop.afficher()
        if (discussion_commencer) :
            text_area.afficher()
            text_area_bis.afficher()
        mettre_a_jour_affichage = False

def verifier_boutons(robot : Robot):
    global mettre_a_jour_affichage, discussion_commencer, text_area, text_area_bis
    if bouton_question.est_actif():
        discussion_commencer = not discussion_commencer
        if discussion_commencer :
            robot.demarrer_discussion()
            bouton_question.ajouter_texte("Arreter la discussion")
        else :
            bouton_question.ajouter_texte("Poser question")
            robot.arreter_discussion()
        mettre_a_jour_affichage = True
    if bouton_stop.est_actif():
        robot.desactiver()
    if discussion_commencer and text_area.est_actif() :
        user_entry = robot.ecrire(text_area)
        print("user_entry = ", user_entry)
        #robot.repondre_question(user_entry)
    if discussion_commencer and text_area_bis.est_actif() :
        user_entry = robot.ecrire(text_area_bis)
        print("user_entry = ", user_entry)
        text_area_bis.effacer_texte()
        #robot.repondre_question(user_entry)

def boucle_programme():
    global discussion_commencer, mettre_a_jour_affichage
    while robot.est_actif():
        events = robot.verifier_evenements()
        if "stop" in events:
            robot.fermer_fenetre()
        elif "C" in events:
            print("Vous appuyez sur C")
        dessiner_fenetre()
        verifier_boutons(robot)
        robot.actualiser_affichage()

if __name__ == "__main__":
    preparer_programme()
    boucle_programme()