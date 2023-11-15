# Auteurs : Mariam Elwa
# date : 15 Novembre 2022
#
#Ce programe créé un logiciel d'édition graphique qui permet a l'utilisateur
#de dessiner des rectangles de différentes tailles et différentes couleurs
#à l'aide de la souris.

setScreenMode(10,10)
taille = 12            # taille du coté des boutons
espace = 6             # taille entre les boutons
couleurs = ["#fff", "#000", "#f00", "#ff0", "#0f0", "#00f", "#f0f"]
# les couleurs possibles à utiliser
couleur = '#fff'       # couleur actuelement choisie
couleurEffacer = '#fff'# couleur initiale de la fenetre(qui suprime)
couleurMenu = '#888'   # couleur du Menu
largeur = 180          # largeur de la fenetre
hauteur = 120         # longeur de la fenetre
hauteurMenu = 24      # longeur de la partie menu
bordure = '#000'       # couleur de la bordure des boutons
imageOriginale = [] # tableau de tableaux qui decrit la couleur de chaque pixel

for i in range(largeur):
    imageOriginale.append(['#888']*(hauteurMenu)+['#fff'] *\
                          (hauteur-hauteurMenu))
    # represent les pixels a l'image initiale de la fenetre

#La fonction creerBoutons retourne un tableau d'enregistrements representant
# les boutons disponibles dans la barre de menu
def creerBoutons(couleurs, taille, espace, couleurEffacer):
    boutonEffacer = struct(coin1=struct(x=espace, y=espace),
                           coin2=struct(x=espace + taille, y=espace + taille),
                           couleur=couleurEffacer, effacer=True)
   # créér le bouton effacer
    boutons = [boutonEffacer]
   # créér les boutons de couleurs qui seront disponibles dans la barre de menu
    for i in range(len(couleurs)):
        bouton = struct(coin1=struct(x=(i + 2) * espace + taille *
                                     (i + 1), y=espace),
                        coin2=struct(x=(i + 2) * espace + taille *
                                     (i + 2), y=espace + taille),
                        couleur=couleurs[i],
                        effacer=False)
        boutons.append(bouton)
    return boutons


# cette fonction prend deux parametres boutons qui est un tableau
# d'enregistrements représentant des boutons et postion qui est un
# enregistrement représentant des coordonnées cartésiennes et retourne
# l'enregistrement contenu dans le tableau boutons si le bouton appartient a la
# position donné.
def trouverBouton(boutons, position):
    for b in boutons:
        if (b.coin1.x <= position.x <= b.coin2.x
                and b.coin1.y <= position.y <= b.coin2.y):
            bouton = b
            return bouton
    return None


# cette fonction prend 3 parametres qui sont:debut qui est un enregistrement
# représentant les coordonnées cartésiennes du clic initial et couleur qui est
# un texte représentant la couleur du rectangle à dessiner et enfin
# imageOriginale est un tableau de tableaux de textes représentant des couleurs
# cette fonction  retourne l animation du  rectangle floattant en fonction de
# la couleur, l enfocement de la souries de l utilisateur.
def dessinerRectangleFlottant(imageOriginale, debut, couleur):
    rectangleFlottant = None #ancien rectangle
    (x0, y0) = (debut.x, debut.y) #point de depart
    while getMouse().button == 1: #tant que le bouton de la souris est enfoncé.
        (x1, y1) = (getMouse().x, getMouse().y); #position actuelle
        y1 = max(y1, hauteurMenu) #les coordonnées sur lesquelles s'étend le
        minX = min(x0, x1)         #rectangle dessiné
        maxX = max(x0, x1) + 1
        minY = min(y0, y1)
        maxY = max(y0, y1) + 1
        fillRectangle(minX, minY, maxX - minX, maxY - minY, couleur)
        #créér le rectangle flottant avec la couleur correspondante
        nouveauRectangle = struct(coin1=struct(x=minX, y=minY),
                                  coin2=struct(x=maxX, y=maxY))
        if rectangleFlottant:
            #surveiller l'etat precedent du rectangle flottant
            for sousSection in trouverSousSections(rectangleFlottant,
                                                   nouveauRectangle):
                restaurerImage(imageOriginale, sousSection)
        rectangleFlottant = nouveauRectangle
        sleep(0.01)
    #une fois le bouton est relaché:
    #Ajouter le rectangle au tableau imageOriginale
    ajouterRectangle(imageOriginale, rectangleFlottant, couleur)
    #dans la fenetre dessin
    fenetreDessin = struct(coin1=struct(x=0, y=hauteurMenu),
                           coin2=struct(x=largeur, y=hauteur))
    #dessiner ce qu'il ya dans le tableau imageOriginale
    restaurerImage(imageOriginale, fenetreDessin)

#Cette fonction retourne un tableau des sous sections
def trouverSousSections(vieuxRect, nouveauRect):
    sousSections = []
    #Si le cote gauche du rectangle flottant est a droite du rectangle
    #flottant precedent
    if nouveauRect.coin1.x > vieuxRect.coin1.x:
        coin1 = struct(x=vieuxRect.coin1.x, y=vieuxRect.coin1.y)
        coin2 = struct(x=nouveauRect.coin1.x, y=vieuxRect.coin2.y)
        #Ajouter la sous-section correspondante
        sousSections.append(struct(coin1=coin1, coin2=coin2))
   #Si le cote droit du rectangle flottant est a gauche du rectangle
   #flottant precedent
    elif nouveauRect.coin2.x < vieuxRect.coin2.x:
        coin1 = struct(x=nouveauRect.coin2.x, y=nouveauRect.coin1.y)
        coin2 = struct(x=vieuxRect.coin2.x, y=nouveauRect.coin2.y)
        #Ajouter la sous-section correspondante
        sousSections.append(struct(coin1=coin1, coin2=coin2))
# Si le haut du rectangle flottant est en dessous du haut du rectangle
# flottant precedent
    if nouveauRect.coin1.y > vieuxRect.coin1.y:
        coin1 = struct(x=vieuxRect.coin1.x, y=vieuxRect.coin1.y)
        coin2 = struct(x=vieuxRect.coin2.x, y=nouveauRect.coin1.y)
        #Ajouter la sous-section correspondante
        sousSections.append(struct(coin1=coin1, coin2=coin2))
# Si le bas du rectangle flottant est au-dessus du bas du rectangle
#flottant precedent
    elif nouveauRect.coin2.y < vieuxRect.coin2.x:
        coin1 = struct(x=vieuxRect.coin1.x, y=nouveauRect.coin2.y)
        coin2 = vieuxRect.coin2
        #Ajouter la sous-section correspondante
        sousSections.append(struct(coin1=coin1, coin2=coin2))

    return sousSections


# cette procedure prend 2 paramètres qui sont: imageOriginale qui est un
# tableau de tableaux de textes représentant des couleurs et rectangle qui est
# un enregistrement des enregistrements qui représentent les coordonnées
#cartésiennes du rectangle dans la grille de pixels.
#Cette procédure dessine une section rectangulaire de l'image imageOriginale
#dans la grille de pixels.
def restaurerImage(imageOriginale, rectangle):
    for X in range(rectangle.coin1.x, rectangle.coin2.x):
        for Y in range(rectangle.coin1.y, rectangle.coin2.y):
            setPixel(X, Y, imageOriginale[X][Y])

#Cette procédure prend 3 paramètres:
# - image: un tableau de tableaux de textes représentant des couleurs
# - rectangle:enregistrement des enregistrements qui représentent les
#coordonnées cartésiennes du rectangle dans la grille de pixels.
# - couleur: couleur du rectangle
# Cette procédure modifie une section rectangulaire de image.
def ajouterRectangle(image, rectangle, couleur):
    for X in range(rectangle.coin1.x, rectangle.coin2.x):
        for Y in range(rectangle.coin1.y, rectangle.coin2.y):
            image[X][Y] = couleur

#Cette procédure efface le dessin
def effacer():
    rect = struct(coin1=struct(x=0, y=hauteurMenu),
                  coin2=struct(x=largeur, y=hauteur))
    fillRectangle(rect.coin1.x, rect.coin1.y, largeur,
                  hauteur - hauteurMenu, couleurEffacer)
    ajouterRectangle(imageOriginale, rect, couleurEffacer)

#Cette procédure réinitialise
def initialiser(boutons):
    setScreenMode(largeur,hauteur)
#Créér la barre de menu
    menuRect = struct(coin1=struct(x=0, y=0),
                      coin2=struct(x=largeur, y=hauteurMenu))
    fillRectangle(menuRect.coin1.x, menuRect.coin1.y,
                  menuRect.coin2.x, menuRect.coin2.y, couleurMenu)
    ajouterRectangle(imageOriginale, menuRect, couleurMenu)

#Créér la fenetre de dessin
    fenetreDessin = struct(coin1=struct(x=0, y=hauteurMenu),
                           coin2=struct(x=largeur, y=hauteur))
    fillRectangle(fenetreDessin.coin1.x, fenetreDessin.coin1.y,
                  fenetreDessin.coin2.x,
                  fenetreDessin.coin2.y - fenetreDessin.coin1.y,couleurEffacer)
    ajouterRectangle(imageOriginale, fenetreDessin, couleurEffacer)
#Créér les boutons pour changer de couleurs
    for bouton in boutons: #Pour chaque bouton
        fillRectangle(bouton.coin1.x, bouton.coin1.y, taille,
                      taille, bouton.couleur)
        for i in range(taille + 1): #Pour les boutons de couleurs
     #changer les contenus des pixel de l'écran simulé a la couleur du bouton
            setPixel(bouton.coin1.x + i, bouton.coin1.y, bordure)
            setPixel(bouton.coin1.x + i, bouton.coin2.y, bordure)
            setPixel(bouton.coin1.x, bouton.coin1.y + i, bordure)
            setPixel(bouton.coin2.x, bouton.coin1.y + i, bordure)
            if bouton.effacer:#Pour le bouton effacer
                setPixel(bouton.coin1.x + i, bouton.coin1.y + i, '#f00')
                setPixel(bouton.coin1.x + i, bouton.coin2.y - i, '#f00')

#Cette procédure attend que l'utilisateur appuie sur le bouton de la souris.
def traiterProchainClic(boutons):
    global couleur
    while True:
        if getMouse().button == 1: #Lorsque l'utilisateur clique sur un pixel
            position = struct(x=getMouse().x, y=getMouse().y)

            if position.y <= hauteurMenu:#calcule si le clic a eu lieu sur un
                                          #bouton ou dans la fenêtre de dessin.
                bouton = trouverBouton(boutons, position)
                if bouton:
                    if bouton.effacer: #effacer le dessin
                        effacer()
                    else:   #couleur du rectangle à dessiner
                        couleur = bouton.couleur
            else: #dessiner un rectangle flottant
                dessinerRectangleFlottant(imageOriginale, position, couleur)
        sleep(0.01)



#Cette procédure démarre l'éditeur graphique.
def dessiner():
    boutons = creerBoutons(couleurs, taille, espace, couleurEffacer)
    initialiser(boutons)
    traiterProchainClic(boutons)

#Cette procédure effectue les tests unitaires des fonctions creerBoutons et
#trouverBouton et les procédures restaurerImage et ajouterRectangle.
def testDessiner():
    assert creerBoutons([], 12, 6, '#fff')==[struct(coin1=struct(x=6, y=6), coin2=struct(x=18, y=18), couleur='#fff', effacer=True)]
    assert creerBoutons(['#ff0','#000'], 12,6,'#fff' )==[struct(coin1=struct(x=6, y=6), coin2=struct(x=18, y=18), couleur='#fff', effacer=True), struct(coin1=struct(x=24, y=6), coin2=struct(x=36, y=18), couleur="#ff0", effacer=False),struct(coin1=struct(x=42, y=6), coin2=struct(x=54, y=18), couleur="#000", effacer=False)]
    assert creerBoutons(['#f0f','#000'], 10, 6, '#fff')==[struct(coin1=struct(x=6, y=6), coin2=struct(x=16, y=16), couleur='#fff', effacer=True), struct(coin1=struct(x=22, y=6), coin2=struct(x=32, y=16), couleur='#f0f', effacer=False),struct(coin1=struct(x=38, y=6), coin2=struct(x=48, y=16), couleur="#000", effacer=False)]
    assert creerBoutons(['#0ff','#000'], 10, 10, '#fff')==[struct(coin1=struct(x=10, y=10), coin2=struct(x=20, y=20), couleur="#fff", effacer=True), struct(coin1=struct(x=30, y=10), coin2=struct(x=40, y=20), couleur="#0ff", effacer=False),struct(coin1=struct(x=50, y=10), coin2=struct(x=60, y=20), couleur="#000", effacer=False)]
    assert creerBoutons(['#fff','#000'], 12, 6, '#999')==[struct(coin1=struct(x=6, y=6), coin2=struct(x=18, y=18), couleur="#999", effacer=True), struct(coin1=struct(x=24, y=6), coin2=struct(x=36, y=18), couleur="#fff", effacer=False),struct(coin1=struct(x=42, y=6), coin2=struct(x=54, y=18), couleur="#000", effacer=False)]

    assert trouverBouton( creerBoutons(['#fff','#000'], 12, 6,'#fff' ),struct(x=0,y=0) )==None
    assert trouverBouton(  creerBoutons(['#fff','#000'], 12, 6,'#fff'),struct(x=6,y=6) )==struct(coin1=struct(x=6, y=6), coin2=struct(x=18, y=18), couleur='#fff', effacer=True)
    assert trouverBouton(  creerBoutons(['#fff','#000'], 12, 6,'#fff'),struct(x=0,y=6) )==None
    assert trouverBouton(  creerBoutons(['#fff','#000'], 12, 6,'#fff'),struct(x=espace,y=0) )==None
    assert trouverBouton(  creerBoutons(['#fff','#000','#222',], 12, 6,'#fff'),struct(x=42,y=6) )==struct(coin1=struct(x=42, y=6), coin2=struct(x=54, y=18), couleur='#000', effacer=False)
    assert trouverBouton( creerBoutons([], 12, 6,'#fff' ),struct(x=6,y=6) )==struct(coin1=struct(x=6, y=6), coin2=struct(x=18, y=18), couleur='#fff', effacer=True)