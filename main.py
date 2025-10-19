# IMPORTATION DES MODULES
import CONFIGS
import turtle
import time

# DEFINITION DE FONCTIONS
def lire_fichier(fichier):
    """"
    Lecture d'un fichier donné en argument et la conversion du contenu du fichier en matrice
    Entrée : nom du fichier
    Résultat : Matrice
    """
    plan_chateau = open(fichier)                 # Ouverture du fichier
    sous_l = []                                  # Variable sous liste = les listes qui sont à l'intérieur de la matrice
    l_prin = []                                  # Variable liste principale =Matrice
    for ligne in plan_chateau:                   # Lecture du fichier
        for element in ligne:
            if element.isdigit() is True:        # On met une condition if pour seulement utiliser les nombres sur le fichier
                sous_l.append(element)
        l_prin.append(sous_l)
        sous_l = []
    plan_chateau.close()
    return l_prin



def calculer_pas(matrice):
    """
    Calcule la dimension à donner aux cases pour que le plan tienne dans la zone de la fenêtre turtle définie
    Entrée : matrice
    Résultat : pas (la dimension des cases)
    """
    global nbr_ligne, nbr_colonne
    for colonne in matrice[0]:              # Calcule le nombre des colonnes dans le plan
        nbr_colonne += 1
    for ligne in matrice:                   # Calcule le nombre des lignes dans le plan
        nbr_ligne += 1
    pas= min((CONFIGS.ZONE_PLAN_MAXI[1]-CONFIGS.ZONE_PLAN_MINI[1])/nbr_ligne, (CONFIGS.ZONE_PLAN_MAXI[0]-CONFIGS.ZONE_PLAN_MINI[0])/nbr_colonne)
    return pas                              # On renvoie le pas minimum pour éviter de sortir de la zone définie


def coordonnes(case,pas):
    """
    Calcule les coordonnées en pixels turtle du coin inférieur gauche d’une case définie par ses coordonnées (numéros
    de ligne et de colonne)
    Entrées : case, pas
    Résultat : coord_case (coordonnées de la case)
    """
    COORD_SUP_GAUCHE = (-240,200)                                    # les coordonnées du coin superior de la zone
    COORD_CASE_00 = (COORD_SUP_GAUCHE[0],COORD_SUP_GAUCHE[1]-pas)     # On trouve les coordonnés de la case (0,0)
    coord_case= (COORD_CASE_00[0]+case[1]*pas, COORD_CASE_00[1]-case[0]*pas)  # On trouve les coord. de la case donné en argument
    return coord_case


def tracer_carre(dimension):
    """
    Trace un carré avec la dimension donné en argument en utilisant Turtle
    Entrée : dimension
    """
    NBR_COTE = 4                    # La nombre de côtés dans un carré
    ANGLE = 360/4                   # L'angle d'un coin du carré
    for i in range(NBR_COTE):       # Traçage du carré
        turtle.forward(dimension)
        turtle.left(ANGLE)


def tracer_case(case, couleur, pas):
    """
    En utilisant la module Turtle, trace un carré de la couleur, taille et aux coordonnés donnés en argument
    Entrées : case, couleur, pas
    """
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(coordonnes(case,pas))                   # Déplacement vers les coordonnés de la case
    turtle.pendown()
    turtle.begin_fill()
    turtle.pen(pencolor=CONFIGS.COULEUR_CASES, fillcolor=couleur, speed=1000)  # Choix de la couleur
    tracer_carre(pas)      # On trace avec la taille(pas) donné
    turtle.end_fill()
    turtle.update()


def afficher_plan(matrice):
    """
    Affiche le plan du chateau en utilisant les données
    Entrée : matrice
    """
    turtle.tracer(0)
    for ligne in matrice:
        for carre in range(len(ligne)):
            code_couleur = ligne[carre]                 # On trouve le code couleur en lisant la matrice
            if code_couleur == '0':                     # '0' = couloir
                couleur = CONFIGS.COULEUR_COULOIR
            elif code_couleur == '1':                   # '1' = mur
                couleur = CONFIGS.COULEUR_MUR
            elif code_couleur == '2':                   # '2' = objectif
                couleur = CONFIGS.COULEUR_OBJECTIF
            elif code_couleur == '3':                   # '3' = porte
                couleur = CONFIGS.COULEUR_PORTE
            elif code_couleur == '4':                   # '4' = objet
                couleur = CONFIGS.COULEUR_OBJET
            case = (matrice.index(ligne), carre)        # on trouve le numéro de la case
            tracer_case(case, couleur, pas)       # on trace le case
    turtle.update()

def dessiner_personnage(mouvement):
    """
    Dessine le personnage dans la case du mouvement voulu.
    Entrée : mouvement
    Return : None
    """
    global pas  # importation de la variable globale pas
    coord_mouvement = coordonnes(mouvement,pas)   # On calcule les coordonnées du mouvement.
    turtle.penup()
    turtle.goto(coord_mouvement[0]+pas/2, coord_mouvement[1]+pas/2)  # On place turtle au milieu de la case
    turtle.pendown()
    turtle.dot(CONFIGS.RATIO_PERSONNAGE * pas, CONFIGS.COULEUR_PERSONNAGE)  # Trace le personnage
    turtle.update()




def ramasser_objet(mouvement):
    global dico_objets, num_objet_obtenu, message, position_actuel
    tracer_case(mouvement, CONFIGS.COULEUR_CASES, pas)
    dessiner_personnage(mouvement)
    position_actuel = mouvement
    message = 'Vous avez trouvé un objet : '+ dico_objets[mouvement]
    afficher_annonce(message)
    num_objet_obtenu += 1
    texte = 'N°' + str(num_objet_obtenu) + ' :  ' + dico_objets[mouvement]
    dessiner_personnage(mouvement)
    inventaire_affichage(texte)
    matrice[mouvement[0]][mouvement[1]] = '0'
    inventaire.add(dico_objets[mouvement])



def deplacer(matrice, position, mouvement):
    """
    La fonction qui decide si le personnage peut se déplacer en lisant la matrice du plan.
    Les cas qui sont possibles : -mouvement = mur/en dehors du plan => rien se passe
                                 -mouvement = couloir => le personnage avance
                                 -mouvement = porte
                                 -mouvement = objet
    Entrées: matrice, position, mouvement
    Return : None
    """
    global nbr_colonne, nbr_ligne,pas, position_actuel, inventaire, dico_objets
    if (matrice[mouvement[0]][mouvement[1]] == '0'):  # cas mouvement est un couloir
        tracer_case(position, CONFIGS.COULEUR_VUE, pas)  # remplissage de la case que le personnage était auparavant
        dessiner_personnage(mouvement)  # nous traçons le personnage à sa nouvelle position
        position_actuel = mouvement     # modification de la position actuel
    elif matrice[mouvement[0]][mouvement[1]] == '4':  # cas mouvement est un objet
        tracer_case(position, CONFIGS.COULEUR_VUE, pas)
        ramasser_objet(mouvement)
    elif matrice[mouvement[0]][mouvement[1]] == '3':
        poser_question(matrice,position,mouvement)
    elif matrice[mouvement[0]][mouvement[1]] == '2':
        tracer_case(position, CONFIGS.COULEUR_VUE, pas)
        dessiner_personnage(mouvement)
        afficher_annonce('Bravo! Vous avez gagné.')
        time.sleep(10)
        exit()

def deplacer_gauche():
    """
    Déplace le personnage une case vers la gauche, si les conditions sont remplies.
    """
    global matrice, position_actuel  # les variables globales
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    mouvement = (position_actuel[0], position_actuel[1]-1)  # trouve la case un pas au gauche
    deplacer(matrice, position_actuel,mouvement)
    turtle.onkeypress(deplacer_gauche, "Left")   # Ré-associe la touche Left à la fonction déplacer_gauche


def deplacer_droite():
    """
    Déplace le personnage une case vers la droite, si les conditions sont remplies.
    """
    global matrice, position_actuel
    turtle.onkeypress(None, "Right")
    mouvement = (position_actuel[0], position_actuel[1]+1)  # trouve la case un pas en droite
    deplacer(matrice, position_actuel,mouvement)
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_bas():
    """
    Déplace le personnage une case vers le bas, si les conditions sont remplies.
    """
    global matrice, position_actuel
    turtle.onkeypress(None, "Down")
    mouvement = (position_actuel[0]+1, position_actuel[1])  # trouve la case un pas en bas
    deplacer(matrice, position_actuel,mouvement)
    turtle.onkeypress(deplacer_bas, "Down")


def deplacer_haut():
    """
    Déplace le personnage une case vers le haut, si les conditions sont remplies.
    """
    global matrice, position_actuel
    turtle.onkeypress(None, "Up")
    mouvement = (position_actuel[0]-1, position_actuel[1])  # trouve la case un pas en haut
    deplacer(matrice, position_actuel,mouvement)
    turtle.onkeypress(deplacer_haut, "Up")


def creer_dictionnaire_des_objets_ou_portes(nom_du_fichier):
    dico = {}
    fichier = open(nom_du_fichier, encoding='utf-8')
    for ligne in fichier:
        ligne = eval(ligne)
        key =ligne[0]
        value = ligne[1]
        dico[key]= value
    fichier.close()
    return dico

def inventaire_affichage(texte):
    global inventaire_coord_affichage
    t_inventaire.penup()
    t_inventaire.goto(inventaire_coord_affichage)
    t_inventaire.pendown()
    t_inventaire.write(texte,font= ('Ariel',9, 'bold'))
    inventaire_coord_affichage = (inventaire_coord_affichage[0],inventaire_coord_affichage[1]-25)


def afficher_annonce(texte):
    t_annonce.clear()
    t_annonce.penup()
    t_annonce.goto(CONFIGS.POINT_AFFICHAGE_ANNONCES)
    t_annonce.pendown()
    t_annonce.write(texte,font=('Ariel',9,'bold'))

def poser_question(matrice,case,mouvement):
    global dico_objets,pas, position_actuel
    afficher_annonce('Cette porte est fermée.')
    reponse = turtle.textinput('Question',dico_portes[mouvement][0])
    turtle.listen()
    if reponse == dico_portes[mouvement][1]:
        afficher_annonce("La porte s'ouvre!")
        matrice[mouvement[0]][mouvement[1]] = '0'
        tracer_case(mouvement,CONFIGS.COULEUR_COULOIR,pas)
        dessiner_personnage(mouvement)
        tracer_case(case,CONFIGS.COULEUR_VUE,pas)
        position_actuel = mouvement
    else:
        afficher_annonce('Mauvaise réponse.')



# CODE PRINCIPAL

inventaire = set()
inventaire_coord_affichage = CONFIGS.POINT_AFFICHAGE_INVENTAIRE
message = ''
t_annonce = turtle.Turtle()
t_annonce.hideturtle()
t_inventaire = turtle.Turtle()
t_inventaire.hideturtle()
position_actuel = CONFIGS.POSITION_DEPART  # la variable qui indique la position actuelle du personnage
nbr_colonne = 0  # nombre de colonnes dans le plan
nbr_ligne = 0    # nombre de lignes dans le plan
num_objet_obtenu = 0

matrice = lire_fichier('plan_chateau.txt')
pas = calculer_pas(matrice)
dico_objets = creer_dictionnaire_des_objets_ou_portes('dico_objets.txt')
dico_portes = creer_dictionnaire_des_objets_ou_portes('dico_portes.txt')

afficher_plan(matrice)
dessiner_personnage(position_actuel)
inventaire_affichage('Inventaire :')


turtle.listen()  # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()  # Place le programme en position d’attente d’une action du joueur
