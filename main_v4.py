#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Version 1 :
        - Déplacement d'un personnage horizontalement et vers le haut (saut)
        - Chargement de plusieurs sprites pour un même mouvement (fluidité)
        - Évolution du personnage dans qun environnement spécifique, avec des bordures bien définies (collisions aux bords)
"""
""" Version 2 :
        - Gestion et affichage des coups de base
"""
""" Version 3 :
        - Gestion et affichage d'un deuxième personnage en local
"""
""" Version 4 :
        - Ajout des options dans le menu d'accueil
        - Ajout du système de gestion de la vie et affichage des barres de vie
        - Ajout du système de déroulement de la partie (rounds)
        - Ajout du système de points et de victoire
        - Modification des sprites de marche en sprites de course
"""

from tkinter import *
from random import randint

def clavier(evenement):
    """Gère les événements associés au clavier"""
    global menu_actif, touches, jeu_actif

    # Si la partie est en cours
    if not menu_actif and jeu_actif:
        # On récupère la touche associée à l'événement
        T = evenement.keysym.upper()

        # Si la touche n'a pas déjà été prise en compte ...
        if T not in touches:
            # ... On l'ajoute à la liste des touches pressées
            touches.append(T)

        # Touches du premier personnage
        if "Q" in touches:
            if deplacement_possibleP1(GAUCHE):
                deplacerP1(GAUCHE)
            else:
                avancer_au_maximumP1(GAUCHE)
        if "D" in touches:
            if deplacement_possibleP1(DROITE):
                deplacerP1(DROITE)
            else:
                avancer_au_maximumP1(DROITE)
        if "Z" in touches:
            if deplacement_possibleP1(HAUT):
                deplacerP1(HAUT)
        if "SPACE" in touches:
            frapperP1()

        # Touches du second personnage
        if "LEFT" in touches:
            if deplacement_possibleP2(GAUCHE):
                deplacerP2(GAUCHE)
            else:
                avancer_au_maximumP2(GAUCHE)
        if "RIGHT" in touches:
            if deplacement_possibleP2(DROITE):
                deplacerP2(DROITE)
            else:
                avancer_au_maximumP2(DROITE)
        if "UP" in touches:
            if deplacement_possibleP2(HAUT):
                deplacerP2(HAUT)
        if "P" in touches:
            frapperP2()

def clavier_relachement(evenement):
    """Gère les événements clavier correspondant au relâchement d'une touche"""
    global menu_actif, jeu_actif

    # Si la partie est en cours
    if not menu_actif and jeu_actif:
        global touches
        
        # On récupère la touche associée à l'événement
        T = evenement.keysym.upper()

        # On supprime la touche relâchée de la liste des touches pressées
        if T in touches:
            touches.remove(T)

        global joueur1, joueur2
        global sprite_a_chargerP1, imagesGaucheP1, imagesDroiteP1, imagesSautGaucheP1, imagesSautDroiteP1, imagesFrappeGaucheP1, imagesFrappeDroiteP1
        global sprite_a_chargerP2, imagesGaucheP2, imagesDroiteP2, imagesSautGaucheP2, imagesSautDroiteP2, imagesFrappeGaucheP2, imagesFrappeDroiteP2
        
        # Si le personnage n'est pas en l'air mais bien sur terre
        if not en_l_airP1:
            if (sprite_a_chargerP1 in imagesGaucheP1) \
            or (sprite_a_chargerP1 in imagesSautGaucheP1) \
            or (sprite_a_chargerP1 in imagesFrappeGaucheP1):
                sprite_a_chargerP1 = imagesGaucheP1[0]
            elif (sprite_a_chargerP1 in imagesDroiteP1) \
            or (sprite_a_chargerP1 in imagesSautDroiteP1) \
            or (sprite_a_chargerP1 in imagesFrappeDroiteP1):
                sprite_a_chargerP1 = imagesDroiteP1[0]
            # Lorsque le personnage est à l'arrêt, ne pas laisser le dernier sprite chargé (= en pleine marche),
            # mais le remplacer par le premier sprite de la direction dans laquelle se déplace le personnage
            canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)
        if not en_l_airP2:    # Si le personnage n'est pas en l'air mais bien sur terre
            if (sprite_a_chargerP2 in imagesGaucheP2) \
            or (sprite_a_chargerP2 in imagesSautGaucheP2) \
            or (sprite_a_chargerP2 in imagesFrappeGaucheP2):
                sprite_a_chargerP2 = imagesGaucheP2[0]
            elif (sprite_a_chargerP2 in imagesDroiteP2) \
            or (sprite_a_chargerP2 in imagesSautDroiteP2) \
            or (sprite_a_chargerP2 in imagesFrappeDroiteP2):
                sprite_a_chargerP2 = imagesDroiteP2[0]
            # Lorsque le personnage est à l'arrêt, ne pas laisser le dernier sprite chargé (= en pleine marche),
            # mais le remplacer par le premier sprite de la direction dans laquelle se déplace le personnage
            canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)

def deplacerP1(direction):
    """Déplace le personnage en fonction de la direction choisie"""
    global joueur1
    global sprite_a_chargerP1, imagesGaucheP1, imagesDroiteP1
    if not menu_actif:
        if direction == GAUCHE or direction == DROITE:
            if direction == GAUCHE:
                # Chargement du bon sprite
                if sprite_a_chargerP1 in imagesGaucheP1:    # Si le déplacement se faisait vers la gauche
                    indice_spriteP1 = imagesGaucheP1.index(sprite_a_chargerP1)
                    sprite_a_chargerP1 = imagesGaucheP1[indice_spriteP1+1] if indice_spriteP1+1 < len(imagesGaucheP1) else imagesGaucheP1[0]
                else:
                    sprite_a_chargerP1 = imagesGaucheP1[0]
                canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)
                # Déplacement du personnage
                val_dep = -DEP_H
                canvas.move(joueur1, val_dep, 0)
            else:
                # Chargement du bon sprite
                if sprite_a_chargerP1 in imagesDroiteP1:    # Si le déplacement se faisait vers la gauche
                    indice_spriteP1 = imagesDroiteP1.index(sprite_a_chargerP1)
                    sprite_a_chargerP1 = imagesDroiteP1[indice_spriteP1+1] if indice_spriteP1+1 < len(imagesDroiteP1) else imagesDroiteP1[0]
                else:
                    sprite_a_chargerP1 = imagesDroiteP1[0]
                canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)
                # Déplacement du personnage
                val_dep = DEP_H
                canvas.move(joueur1, val_dep, 0)
        elif direction == HAUT:
            sauterP1()

def deplacerP2(direction):
    """Déplace le personnage en fonction de la direction choisie"""
    global joueur2
    global sprite_a_chargerP2, imagesGaucheP2, imagesDroiteP2
    if not menu_actif:
        if direction == GAUCHE or direction == DROITE:
            if direction == GAUCHE:
                # Chargement du bon sprite
                if sprite_a_chargerP2 in imagesGaucheP2:    # Si le déplacement se faisait vers la gauche
                    indice_spriteP2 = imagesGaucheP2.index(sprite_a_chargerP2)
                    sprite_a_chargerP2 = imagesGaucheP2[indice_spriteP2+1] if indice_spriteP2+1 < len(imagesGaucheP2) else imagesGaucheP2[0]
                else:
                    sprite_a_chargerP2 = imagesGaucheP2[0]
                canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)
                # Déplacement du personnage
                val_dep = -DEP_H
                canvas.move(joueur2, val_dep, 0)
            else:
                # Chargement du bon sprite
                if sprite_a_chargerP2 in imagesDroiteP2:    # Si le déplacement se faisait vers la gauche
                    indice_spriteP2 = imagesDroiteP2.index(sprite_a_chargerP2)
                    sprite_a_chargerP2 = imagesDroiteP2[indice_spriteP2+1] if indice_spriteP2+1 < len(imagesDroiteP2) else imagesDroiteP2[0]
                else:
                    sprite_a_chargerP2 = imagesDroiteP2[0]
                canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)
                # Déplacement du personnage
                val_dep = DEP_H
                canvas.move(joueur2, val_dep, 0)
        elif direction == HAUT:
            sauterP2()

def avancer_au_maximumP1(direction):
    """Déplace le personnage le plus possible vers une limite"""
    global joueur1

    # On récupère l'abscisse du joueur
    abscisse = list(canvas.coords(joueur1))[0]

    if direction == GAUCHE:
        val_dep = -abscisse    # La valeur de déplacement correspond à l'opposé de l'abscisse du perso (distance entre l'extrêmité gauche et le perso = son abscisse)
        canvas.move(joueur1, val_dep, 0)
    elif direction == DROITE:
        val_dep = DIM_FEN[0] - (abscisse + DIM_PERSO[0])  # La valeur de déplacement est la distance (1080 - abscisse du perso)
        canvas.move(joueur1, val_dep, 0)

def avancer_au_maximumP2(direction):
    """Déplace le personnage le plus possible vers une limite"""
    global joueur2

    # On récupère l'abscisse du joueur
    abscisse = list(canvas.coords(joueur2))[0]

    if direction == GAUCHE:
        val_dep = -abscisse    # La valeur de déplacement correspond à l'opposé de l'abscisse du perso (distance entre l'extrêmité gauche et le perso = son abscisse)
        canvas.move(joueur2, val_dep, 0)
    elif direction == DROITE:
        val_dep = DIM_FEN[0] - (abscisse + DIM_PERSO[0])  # La valeur de déplacement est la distance (1080 - abscisse du perso)
        canvas.move(joueur2, val_dep, 0)

def sauterP1():
    """Gère le saut du personnage"""
    global joueur1
    global en_l_airP1
    global sprite_a_chargerP1, imagesGaucheP1, imagesDroiteP1, imagesSautGaucheP1, imagesSautDroiteP1

    # Si le personnage n'est pas en l'air
    if not en_l_airP1:
        # Détermination de la direction avant le saut
        direction_precedente = GAUCHE if (sprite_a_chargerP1 in imagesGaucheP1 or sprite_a_chargerP1 in imagesSautGaucheP1 or sprite_a_chargerP1 in imagesFrappeGaucheP1) else DROITE
        # Déplacement du personnage
        canvas.move(joueur1, 0, -DEP_V)
        en_l_airP1 = True
        # Chargement du sprite de saut
        sprite_a_chargerP1 = imagesSautGaucheP1[1] if direction_precedente == GAUCHE else imagesSautDroiteP1[1]
        canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)

        fenetre.after(225, redescendreP1) # Appel de la fonction "redescendre" au bout de 225ms

def sauterP2():
    """Gère le saut du personnage"""
    global joueur2
    global en_l_airP2
    global sprite_a_chargerP2, imagesGaucheP2, imagesDroiteP2, imagesSautGaucheP2, imagesSautDroiteP2

    # Si le personnage n'est pas en l'air
    if not en_l_airP2:
        # Détermination de la direction avant le saut
        direction_precedente = GAUCHE if (sprite_a_chargerP2 in imagesGaucheP2 or sprite_a_chargerP2 in imagesSautGaucheP2 or sprite_a_chargerP2 in imagesFrappeGaucheP2) else DROITE
        # Déplacement du personnage
        canvas.move(joueur2, 0, -DEP_V)
        en_l_airP2 = True
        # Chargement du sprite de saut
        sprite_a_chargerP2 = imagesSautGaucheP2[1] if direction_precedente == GAUCHE else imagesSautDroiteP2[1]
        canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)

        fenetre.after(225, redescendreP2) # Appel de la fonction "redescendre" au bout de 225ms

def redescendreP1():
    """Gère la descente du personnage après un saut"""
    global joueur1
    global en_l_airP1
    global sprite_a_chargerP1, imagesGaucheP1, imagesDroiteP1, imagesSautGaucheP1, imagesSautDroiteP1

    # Si le personnage est en l'air
    if en_l_airP1:
        # Déplacement du personnage
        canvas.move(joueur1, 0, DEP_V)
        en_l_airP1 = False

        # Détermination de la direction avant le saut
        if (sprite_a_chargerP1 in imagesGaucheP1) \
        or (sprite_a_chargerP1 in imagesSautGaucheP1) \
        or (sprite_a_chargerP1 in imagesFrappeGaucheP1):
            direction_precedente = GAUCHE
        elif (sprite_a_chargerP1 in imagesDroiteP1) \
        or (sprite_a_chargerP1 in imagesSautDroiteP1) \
        or (sprite_a_chargerP1 in imagesFrappeDroiteP1):
            direction_precedente = DROITE

        # Chargement du bon sprite
        sprite_a_chargerP1 = imagesGaucheP1[0] if direction_precedente == GAUCHE else imagesDroiteP1[0]
        canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)

def redescendreP2():
    """Gère la descente du personnage après un saut"""
    global joueur2
    global en_l_airP2
    global sprite_a_chargerP2, imagesGaucheP2, imagesDroiteP2, imagesSautGaucheP2, imagesSautDroiteP2

    # Si le personnage est en l'air
    if en_l_airP2:
        # Déplacement du personnage
        canvas.move(joueur2, 0, DEP_V)
        en_l_airP2 = False
        # Détermination de la direction avant le saut
        if (sprite_a_chargerP2 in imagesGaucheP2) \
        or (sprite_a_chargerP2 in imagesSautGaucheP2) \
        or (sprite_a_chargerP2 in imagesFrappeGaucheP2):
            direction_precedente = GAUCHE
        elif (sprite_a_chargerP2 in imagesDroiteP2) \
        or (sprite_a_chargerP2 in imagesSautDroiteP2) \
        or (sprite_a_chargerP2 in imagesFrappeDroiteP2):
            direction_precedente = DROITE
        # Chargement du bon sprite
        sprite_a_chargerP2 = imagesGaucheP2[0] if direction_precedente == GAUCHE else imagesDroiteP2[0]
        canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)

def deplacement_possibleP1(direction):
    """Vérifie que le mouvement dans la direction choisie est possible"""
    global joueur1

    # Récupération de l'abscisse du joueur
    abscisse = list(canvas.coords(joueur1))[0]

    # Vérifie si le déplacement fait sortir le joueur de la zone jouable
    if (direction == GAUCHE and abscisse - DEP_H < 0) \
    or (direction == DROITE and abscisse + DIM_PERSO[0] + DEP_H > DIM_JOUABLE[0]):
        return False

    return True

def deplacement_possibleP2(direction):
    """Vérifie que le mouvement dans la direction choisie est possible"""
    global joueur2

    # Récupération de l'abscisse du joueur
    abscisse = list(canvas.coords(joueur2))[0]

    # Vérifie si le déplacement fait sortir le joueur de la zone jouable ...
    if (direction == GAUCHE and abscisse - DEP_H < 0) \
    or (direction == DROITE and abscisse + DIM_PERSO[0] + DEP_H > DIM_JOUABLE[0]):
        return False
    return True

def frapperP1():
    """Affiche le(s) sprite(s) de coup"""
    global joueur1
    global sprite_a_chargerP1, imagesGaucheP1, imagesDroiteP1, imagesFrappeGaucheP1, imagesFrappeDroiteP1
    global en_cours_attaqueP1
    global vie_p2, jeu_actif, point_p1

    # On récupère la direction du personnage avant le coup
    if (sprite_a_chargerP1 in imagesGaucheP1) \
    or (sprite_a_chargerP1 in imagesFrappeGaucheP1) \
    or (sprite_a_chargerP1 in imagesSautGaucheP1):
        direction_precedente = GAUCHE
    elif (sprite_a_chargerP1 in imagesDroiteP1) \
    or (sprite_a_chargerP1 in imagesFrappeDroiteP1) \
    or (sprite_a_chargerP1 in imagesSautDroiteP1):
        direction_precedente = DROITE

    # Si le personnage n'est pas déjà en cours d'attaque
    if not en_cours_attaqueP1:
        # On charge l'image de frappe dans la bonne direction
        sprite_a_chargerP1 = imagesFrappeGaucheP1[1] if direction_precedente == GAUCHE else imagesFrappeDroiteP1[1]
        canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)

        # On modifie la variable globale -> le personnage est en cours d'attaque
        en_cours_attaqueP1 = True

        # Si la partie est en cours
        if jeu_actif:
            # S'il y a collision des deux joueurs
            if collisions():
                # On inflige des dégâts à l'autre joueur
                degats = randint(8,12)
                if (vie_p2 - degats) > 0:
                    vie_p2 -= degats
                else:
                    vie_p2 = 0

                    # On augmente le score du joueur
                    point_p1 += 1

                    # On passe au round suivant
                    rounds()

                # On met à jour la barre de vie
                canvas.coords(barre_p2, 800, 40, 800+vie_p2, 70)

                # On affiche une couleur différente pour la barre de vie selon la vie restante
                if 150 < vie_p2 <= 191:
                    canvas.itemconfigure(barre_p2, fill="#C6E501")
                if 100 < vie_p2 <= 150:
                    canvas.itemconfigure(barre_p2, fill="yellow")
                if 50 < vie_p2 <= 100:
                    canvas.itemconfigure(barre_p2, fill="orange")
                if 0 < vie_p2 <= 50:
                    canvas.itemconfigure(barre_p2, fill="red")

    # Sinon, si le personnage est en cours d'attaque
    else:
        # On charge l'image de marche dans la bonne direction
        sprite_a_chargerP1 = imagesGaucheP1[0] if direction_precedente == GAUCHE else imagesDroiteP1[0]
        canvas.itemconfigure(joueur1, image=sprite_a_chargerP1)

        # On modifie la variable globale -> le personnage n'est plus en cours d'attaque
        en_cours_attaqueP1 = False

    # Si le personnage est en cours d'attaque
    # -> appel de la fonction après un certain délai
    if en_cours_attaqueP1:
        fenetre.after(200, frapperP1)

def frapperP2():
    """Affiche le(s) sprite(s) de coup"""
    global joueur2
    global sprite_a_chargerP2, imagesGaucheP2, imagesDroiteP2, imagesFrappeGaucheP2, imagesFrappeDroiteP2
    global en_cours_attaqueP2
    global vie_p1, jeu_actif, point_p2

    # On récupère la direction du personnage avant le coup
    if (sprite_a_chargerP2 in imagesGaucheP2) \
    or (sprite_a_chargerP2 in imagesFrappeGaucheP2) \
    or (sprite_a_chargerP2 in imagesSautGaucheP2):
        direction_precedente = GAUCHE
    elif (sprite_a_chargerP2 in imagesDroiteP2) \
    or (sprite_a_chargerP2 in imagesFrappeDroiteP2) \
    or (sprite_a_chargerP2 in imagesSautDroiteP2):
        direction_precedente = DROITE

    # Si le personnage n'est pas déjà en cours d'attaque
    if not en_cours_attaqueP2:
        # On charge l'image de frappe dans la bonne direction
        sprite_a_chargerP2 = imagesFrappeGaucheP2[1] if direction_precedente == GAUCHE else imagesFrappeDroiteP2[1]
        canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)

        # On modifie la variable globale -> le personnage est en cours d'attaque
        en_cours_attaqueP2 = True

        # Si la partie est en cours
        if jeu_actif:
            # S'il y a collision des deux joueurs
            if collisions():
                # On inflige des dégâts à l'autre joueurs
                degats = randint(8,12)
                if (vie_p1 - degats) > 0:
                    vie_p1 -= degats
                else:
                    vie_p1 = 0

                    # On augmente le score du joueur
                    point_p2 += 1

                    # On passe au round suivant
                    rounds()

                # On met à jour la barre de vie
                canvas.coords(barre_p1,80,40,80+vie_p1,70)

                # On affiche une couleur différente pour la barre de vie selon la vie restante
                if 150 < vie_p1 <= 191:
                    canvas.itemconfigure(barre_p1, fill="#C6E501")
                if 100 < vie_p1 <= 150:
                    canvas.itemconfigure(barre_p1, fill="yellow")
                if 50 < vie_p1 <= 100:
                    canvas.itemconfigure(barre_p1, fill="orange")
                if 0 < vie_p1 <= 80:
                    canvas.itemconfigure(barre_p1, fill="red")
    # Sinon, si le personnage est en cours d'attaque
    else:
        # On charge l'image de marche dans la bonne direction
        sprite_a_chargerP2 = imagesGaucheP2[0] if direction_precedente == GAUCHE else imagesDroiteP2[0]
        canvas.itemconfigure(joueur2, image=sprite_a_chargerP2)

        # On modifie la variable globale -> le personnage n'est plus en cours d'attaque
        en_cours_attaqueP2 = False

    # Si le personnage est en cours d'attaque
    # -> appel de la fonction après un certain délai
    if en_cours_attaqueP2:
        fenetre.after(200, frapperP2)

def afficher_menu_accueil():
    """Affiche le menu"""
    global image_menu, bt_jouer, bt_options, bt_quitter, txt_jouer, txt_options, txt_quitter, image_fond_menu

    # Si le menu est affiché
    if menu_actif:
        # Affichage du fond
        image_menu = canvas.create_image(0, 0, anchor="nw", image=image_fond_menu)

        # Affichage du bouton et du texte de lancement de partie
        bt_jouer = canvas.create_rectangle(408, 287, 672, 363, fill='red', activefill='blue')
        txt_jouer = canvas.create_text(540, 325, text="Jouer", font='Helvetica 40', state="disabled")

        # Affichage du bouton et du texte d'options
        bt_options = canvas.create_rectangle(408, 386, 672, 462, fill='red', activefill='blue')
        txt_options = canvas.create_text(540, 424, text="Options", font='Helvetica 40', state="disabled")

        # Affichage du bouton et du texte de fermeture du jeu
        bt_quitter = canvas.create_rectangle(408, 485, 672, 561, fill='red', activefill='blue')
        txt_quitter = canvas.create_text(540, 523, text="Quitter", font='Helvetica 40', state="disabled")

def souris(event):
    """Gère les événements souris"""
    global menu_actif, jeu_actif, menu_options_actif, menu_fin_actif
    global image_fond
    global point_p1, point_p2, vie_p1, vie_p2, pseudo_j1, pseudo_j2
    global txt_pseudo_j1, txt_pseudo_j2, bt_ville, txt_ville, bt_roches, txt_roches, bt_neige, txt_neige, bt_foret, txt_foret, bt_retour, txt_retour, txt_pseudos, txt_map, fen_pseudo1, fen_pseudo2

    # Si le menu actif est celui d'accueil
    if menu_actif:
        # Si le clic s'effectue au niveau du bouton "Jouer"
        if ((408 <= event.x <= 672) and (287 <= event.y <= 363)):
            # Met à jour la variable d'état du menu d'accueil
            menu_actif = False

            # Met jour la variabel d'état de la partie
            jeu_actif = True

            # Supprime les éléments du menu d'accueil
            canvas.delete(image_menu, bt_jouer, bt_options, bt_quitter, txt_jouer, txt_options, txt_quitter)

            # Affiche la partie
            affichage()
        # Si le clic s'effectue au niveau du bouton "Options"
        elif ((408 <= event.x <= 672) and (386 <= event.y <= 462)):
            # Met à jour la variable d'état du menu d'accueil
            menu_actif = False

            # Supprime les éléments du menu d'accueil
            canvas.delete(bt_jouer, bt_options, bt_quitter, txt_jouer, txt_options, txt_quitter)

            # Affiche le menu d'options
            afficher_menu_options()
        # Si le clic s'effectue au niveau du bouton "Quitter"
        elif ((408 <= event.x <= 672) and (485 <= event.y <= 561)):
            # Ferme la fenêtre
            fenetre.destroy()

    # Si le menu actif est celui des options
    if menu_options_actif:
        # Fond de "ville"
        if ((108 <= event.x <= 372) and (238 <= event.y <= 314)):
            image_fond = PhotoImage(file="img/decor/ville.gif")
        # Fond de "pierre"
        elif ((108 <= event.x <= 372) and (337 <= event.y <= 413)):
            image_fond = PhotoImage(file="img/decor/roches.gif")
        # Fond de "neige"
        elif ((108 <= event.x <= 372) and (436 <= event.y <= 512)):
            image_fond = PhotoImage(file="img/decor/neige.gif")
        # Fond de "forêt"
        elif ((108 <= event.x <= 372) and (535 <= event.y <= 611)):
            image_fond = PhotoImage(file="img/decor/foret.gif")
        # Clic sur le  bouton de retour au menu
        elif ((408 <= event.x <= 672) and (634 <= event.y <= 710)):
            pseudo_j1 = txt_pseudo_j1.get("1.0", "end-1c") # On récupère ce qui a été inscrit dans le champ de saisie des pseudos (à partir du caractère se trouvant à la première ligne et en position 0
            pseudo_j2 = txt_pseudo_j2.get("1.0", "end-1c") # jusqu'à la fin du champ moins 1 caractère pour éviter le saut de ligne)

            # Supprime les éléments du menu d'options
            canvas.delete(bt_ville, txt_ville, bt_roches, bt_foret, bt_neige, txt_roches, txt_neige, txt_foret, txt_pseudos, txt_map, fen_pseudo1, fen_pseudo2, txt_pseudo_j1, txt_pseudo_j2)

            # Met à jour les variables d'état du menu d'accueil et du menu d'options
            menu_options_actif = False
            menu_actif = True

            # Affichage du menu d'accueil
            afficher_menu_accueil()

    # Si le menu actif est celui de fin de partie
    if menu_fin_actif:
        # Si le clic sur le bouton "Rejouer"
        if ((408 <= event.x <= 672) and (287 <= event.y <= 363)):
            # Met à jour les variables d'état
            menu_actif = False
            jeu_actif = True

            # Supprime les éléments du menu de fin de partie
            canvas.delete(bt_rejouer, bt_menu, bt_quitter, txt_rejouer, txt_menu, txt_quitter, vainqueur)

            # Réinitialise les caractéristiques des joueurs (vie, points)
            vie_p1 = 200
            vie_p2 = 200
            point_p1 = 0
            point_p2 = 0

            # Affiche la partie
            affichage()
        # Si le clique s'effectue au niveau du bouton "Menu"
        elif ((408 <= event.x <= 672) and (386 <= event.y <= 462)):
            # Réinitialise les caractéristiques des joueurs (vie, score)
            vie_p1 = 200
            vie_p2 = 200
            point_p1 = 0
            point_p2 = 0

            # Supprime les éléments du menu de fin de partie
            canvas.delete(bt_rejouer, bt_menu, bt_quitter, txt_rejouer, txt_menu, txt_quitter, vainqueur)

            # Met à jour les variables d'état des menus de fin de partie et d'accueil
            menu_fin_actif = False
            menu_actif = True

            # Affiche le menu
            afficher_menu_accueil()
        # Si le clic s'effectue au niveau du bouton "Quitter"
        elif ((408 <= event.x <= 672) and (485 <= event.y <= 561)):
            # Ferme la fenêtre
            fenetre.destroy()

def affichage():
    """Affiche le terrain, ses composants et les personnages"""
    global joueur1, joueur2
    global image_fond, sol
    global vie_p1, vie_p2, score_p1, score_p2, nom_j1, nom_j2
    global barre_p1, barre_p2, contour1, contour2, image_sol

    # Si la partie est en cours
    if not menu_actif:
        # Affichage du fond
        fond_jeu = canvas.create_image(0, 0, anchor="nw", image=image_fond)

        # Affichage du personnage
        joueur1 = canvas.create_image(20, DIM_JOUABLE[1]-DIM_PERSO[1], image=sprite_a_chargerP1, anchor="nw")
        joueur2 = canvas.create_image(1000, DIM_JOUABLE[1]-DIM_PERSO[1], image=sprite_a_chargerP2, anchor="nw")

        # Affichage du sol
        sol = []
        for i in range(4):
            sol.append(canvas.create_image(i * 270, 571, anchor="nw", image=image_sol))

        # Affichage des barres de vie
        contour1 = canvas.create_rectangle(79,39,280,70, outline='red')
        contour2 = canvas.create_rectangle(799,39,1000,70, outline='red')
        barre_p1 = canvas.create_rectangle(80,40,80+vie_p1,70, fill='green', width=0)
        barre_p2 = canvas.create_rectangle(800,40,800+vie_p2,70, fill='green', width=0)

        # Affichage des scores
        score_p1 = canvas.create_text(50,55,text = str(point_p1), font = 'Heltvica 20')
        score_p2 = canvas.create_text(1029,55,text = str(point_p2), font = 'Heltvica 20')

        # Affichage des noms
        nom_j1 = canvas.create_text(180,25, text = pseudo_j1, font = "Helvetica 20")
        nom_j2 = canvas.create_text(900,25, text = pseudo_j2, font = "Helvetica 20")

def collisions():
    """Vérifie si les joueurs se superposent"""
    global joueur1, joueur2
    global menu_actif, jeu_actif
    global en_l_airP1, en_l_airP2

    # Si la partie est en cours
    if not menu_actif and jeu_actif:
        # Si les joueurs sont bien à terre
        if not en_l_airP1 and not en_l_airP2:
            # On récupère les abscisses des joueurs
            abscisses = [ list(canvas.coords(joueur1))[0], list(canvas.coords(joueur2))[0] ]

            # Si l'écart entre deux joueurs est inférieur à la largeur du joueur
            if abs(abscisses[0] - abscisses[1]) <= DIM_PERSO[0]:
                return True

        return False

def rounds():
    """Gère le déroulement de la partie"""
    global vie_p1, vie_p2, score_p1, score_p2
    global joueur1, joueur2, joueur_gagnant
    global point_p1, point_p2
    global jeu_actif

    # Si aucun des joueurs n'a atteint le score de 3 points ...
    if (point_p1 < 3 and point_p2 < 3):
        # ... et si l'un des joueurs n'est plus en vie
        if vie_p1 == 0 or vie_p2 == 0:
            # ... on modifie met à jour le texte indiquant le score du joueur étant encore en vie
            if vie_p1 == 0:
                canvas.itemconfigure(score_p2, text = point_p2)
            else:
                canvas.itemconfigure(score_p1, text = point_p1)

        # 0n restaure la vie des joueurs et on modifie la barre de vie
        vie_p1 = vie_p2 = 200
        canvas.coords(barre_p1,80,40,80+vie_p1,70)
        canvas.itemconfigure(barre_p1, fill="green")
        canvas.coords(barre_p2,800,40,800+vie_p2,70)
        canvas.itemconfigure(barre_p2, fill="green")

        # On replace les joueurs à leurs coordonnées de départ
        canvas.coords(joueur1,20,DIM_JOUABLE[1]-DIM_PERSO[1])
        canvas.coords(joueur2,1000,DIM_JOUABLE[1]-DIM_PERSO[1])
    else:
        # On modifie la variable d'état de la partie
        jeu_actif = False

        # On détermine le pseudo du joueur gagnant
        joueur_gagnant = pseudo_j1 if vie_p2 == 0 else pseudo_j2

        # On lance le menu de fin
        afficher_menu_fin()

def afficher_menu_options():
    """Affiche le menu d'options"""
    global menu_options_actif
    global txt_pseudo_j1, txt_pseudo_j2
    global bt_ville, txt_ville, bt_roches, txt_roches, bt_neige, txt_neige, bt_foret, txt_foret, bt_retour, txt_retour, txt_pseudos, txt_map, txt_pseudo_j1, txt_pseudo_j2, fen_pseudo1, fen_pseudo2

    # On modifie la variable d'état du menu d'options
    menu_options_actif = True

    # Affichage du bouton et du texte du fond "ville"
    bt_ville = canvas.create_rectangle(108, 238, 372, 314, fill='red', activefill='blue')
    txt_ville = canvas.create_text(240, 276, text="Ville", font='Helvetica 30', state="disabled")

    # Affichage du bouton et du texte du fond "roches"
    bt_roches = canvas.create_rectangle(108, 337, 372, 413, fill='red', activefill='blue')
    txt_roches = canvas.create_text(240, 375, text="Roches", font='Helvetica 30', state="disabled")

    # Affichage du bouton et du texte du fond "neige"
    bt_neige = canvas.create_rectangle(108, 436, 372, 512, fill='red', activefill='blue')
    txt_neige = canvas.create_text(240, 474, text="Neige", font='Helvetica 30', state="disabled")

    # Affichage du bouton et du texte du fond "forêt"
    bt_foret = canvas.create_rectangle(108, 535, 372, 611, fill='red', activefill='blue')
    txt_foret = canvas.create_text(240, 573, text="Forêt", font='Helvetica 30', state="disabled")

    # Affichage du bouton et du texte de retour
    bt_retour = canvas.create_rectangle(408, 634, 672, 710, fill='red', activefill='blue')
    txt_retour = canvas.create_text(540, 672, text="Retour", font='Helvetica 30', state="disabled")

    # Affichage des zones de saisie des pseudos
    txt_pseudo_j1 = Text(canvas, font="Helvetica 30")
    txt_pseudo_j1.insert(INSERT, pseudo_j1)                   # Affiche le pseudo par défaut
    txt_pseudo_j2 = Text(canvas, font="Helvetica 30")
    txt_pseudo_j2.insert(INSERT, pseudo_j2)
    fen_pseudo1 = canvas.create_window(840, 276, window=txt_pseudo_j1, width=264, height=50) # Fenêtre qui contient le champ de saisie (widget Text)
    fen_pseudo2 = canvas.create_window(840, 375, window=txt_pseudo_j2, width=264, height=50) # Fenêtre qui contient le champ de saisie (widget Text)

    # Affiche les indications concernant les options
    txt_pseudos = canvas.create_text(840, 200, text="Modifier les pseudos :", font='Helvetica 30', state="disabled")
    txt_map = canvas.create_text(240, 200, text="Modifier la map :", font='Helvetica 30', state="disabled")

def afficher_menu_fin():
    global menu_actif, jeu_actif, menu_fin_actif
    global joueur_gagnant, vainqueur
    global score_p1, score_p2, point_p1, point_p2, nom_j1, nom_j2
    global touches
    global bt_rejouer, txt_rejouer, bt_menu, txt_menu, bt_quitter, txt_quitter

    # Si la partie est en cours
    if not menu_actif and not jeu_actif:
        # On supprime les éléments de l'interface de combat
        global joueur1, joueur2, contour1, contour2, barre_p1, barre_p2, score_p2, score_p2, nom_j1, nom_j2
        canvas.delete(joueur1, joueur2, contour1, contour2, barre_p1, barre_p2, score_p1, score_p2, nom_j1, nom_j2)
        for i in sol:
            canvas.delete(i)

        # On affiche le message de victoire
        vainqueur = canvas.create_text(540, 45, text="Le joueur gagnant est " + joueur_gagnant + " avec un score de " + str(point_p1) + "-" + str(point_p2), font='Helvetica 30')

        # On affiche le bouton et le texte pour "Rejouer"
        bt_rejouer = canvas.create_rectangle(408, 287, 672, 363, fill='red', activefill='blue')
        txt_rejouer = canvas.create_text(540, 325, text="Rejouer", font='Helvetica 50', state="disabled")

        # On affiche le bouton et le texte pour "Menu"
        bt_menu = canvas.create_rectangle(408, 386, 672, 462, fill='red', activefill='blue')
        txt_menu = canvas.create_text(540, 424, text="Menu", font='Helvetica 50', state="disabled")

        # On affiche le bouton et le texte pour "Quitter"
        bt_quitter = canvas.create_rectangle(408, 485, 672, 561, fill='red', activefill='blue')
        txt_quitter = canvas.create_text(540, 523, text="Quitter", font='Helvetica 50', state="disabled")

        # On réinitialise la liste contenant les touches au cas où la partie se serait terminée alors qu'un joueur maintenait enfoncée une touche du clavier
        touches = []

        # On met à jour la variable d'état du menu de fin de partie
        menu_fin_actif = True

# Constantes
    # Dimensions
DIM_FEN = (1080, 720)
DIM_PERSO = (35, 60)
DIM_JOUABLE = (1080, 571)

    # Directions possibles des personnages
GAUCHE = 0
DROITE = 1
HAUT = 2
BAS = 3

    # Valeurs de déplacement horizontal et vertical des personnages
DEP_H = 14
DEP_V = 60

    # Maximum de points de vie des personnages
VIE_MAX = 200

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("TkSmash - Fight for Glory")
fenetre.geometry("{}x{}".format(DIM_FEN[0], DIM_FEN[1]))
fenetre.resizable(width=False, height=False)

# Création du canvas
canvas = Canvas(fenetre, width=DIM_FEN[0], height=DIM_FEN[1], bg="white")
canvas.pack()

# Chargement des sprites du perso_1
    # Sprites vers la gauche
cheminImagesGaucheP1 = ["img/perso/1/course/CG/CG{}.gif".format(i+1) for i in range(9)]
imagesGaucheP1 = list()
for cheminP1 in cheminImagesGaucheP1:
    imagesGaucheP1.append( PhotoImage(file=cheminP1) )

    # Sprites vers la droite
cheminImagesDroiteP1 = ["img/perso/1/course/CD/CD{}.gif".format(i+1) for i in range(9)]
imagesDroiteP1 = list()
for cheminP1 in cheminImagesDroiteP1:
    imagesDroiteP1.append( PhotoImage(file=cheminP1) )

    # Sprites vers le haut
cheminImagesSautGaucheP1 = ["img/perso/1/saut/G/{}.gif".format(i+1) for i in range(2)]
cheminImagesSautDroiteP1 = ["img/perso/1/saut/D/{}.gif".format(i+1) for i in range(2)]
imagesSautGaucheP1, imagesSautDroiteP1 = list(), list()
for cheminP1 in cheminImagesSautGaucheP1:
    imagesSautGaucheP1.append( PhotoImage(file=cheminP1) )
for cheminP1 in cheminImagesSautDroiteP1:
    imagesSautDroiteP1.append( PhotoImage(file=cheminP1) )

 # Sprite combat
cheminImagesFrappeGaucheP1 = ["img/perso/1/frappe/CG/{}.gif".format(i+1) for i in range(2)]
cheminImagesFrappeDroiteP1 = ["img/perso/1/frappe/CD/{}.gif".format(i+1) for i in range(2)]
imagesFrappeGaucheP1, imagesFrappeDroiteP1 = list(), list()
for cheminP1 in cheminImagesFrappeGaucheP1:
    imagesFrappeGaucheP1.append( PhotoImage(file=cheminP1) )
for cheminP1 in cheminImagesFrappeDroiteP1:
    imagesFrappeDroiteP1.append( PhotoImage(file=cheminP1) )



# Chargement des sprites du perso_2
    # Sprites vers la gauche
cheminImagesGaucheP2 = ["img/perso/2/course/CG/CG{}.gif".format(i+1) for i in range(9)]
imagesGaucheP2 = list()
for cheminP2 in cheminImagesGaucheP2:
    imagesGaucheP2.append( PhotoImage(file=cheminP2) )

    # Sprites vers la droite
cheminImagesDroiteP2 = ["img/perso/2/course/CD/CD{}.gif".format(i+1) for i in range(9)]
imagesDroiteP2 = list()
for cheminP2 in cheminImagesDroiteP2:
    imagesDroiteP2.append( PhotoImage(file=cheminP2) )

    # Sprites vers le haut
cheminImagesSautGaucheP2 = ["img/perso/2/saut/G/SG{}.gif".format(i+1) for i in range(2)]
cheminImagesSautDroiteP2 = ["img/perso/2/saut/D/SD{}.gif".format(i+1) for i in range(2)]
imagesSautGaucheP2, imagesSautDroiteP2 = list(), list()
for cheminP2 in cheminImagesSautGaucheP2:
    imagesSautGaucheP2.append( PhotoImage(file=cheminP2) )
for cheminP2 in cheminImagesSautDroiteP2:
    imagesSautDroiteP2.append( PhotoImage(file=cheminP2) )

 # Sprite combat
cheminImagesFrappeGaucheP2 = ["img/perso/2/frappe/G/FG{}.gif".format(i+1) for i in range(2)]
cheminImagesFrappeDroiteP2 = ["img/perso/2/frappe/D/FD{}.gif".format(i+1) for i in range(2)]
imagesFrappeGaucheP2, imagesFrappeDroiteP2 = list(), list()
for cheminP2 in cheminImagesFrappeGaucheP2:
    imagesFrappeGaucheP2.append( PhotoImage(file=cheminP2) )
for cheminP2 in cheminImagesFrappeDroiteP2:
    imagesFrappeDroiteP2.append( PhotoImage(file=cheminP2) )


# Variables globales
    # Booléens vérifiant si le personnage (P1 ou P2) est en l'air
en_l_airP1 = False
en_l_airP2 = False

    # Booléens vérifiant si un menu est actif
menu_actif          = True                          # Menu d'accueil
menu_options_actif  = False                         # Menu d'options
menu_fin_actif      = False                         # Menu de fin de partie

    # Booléen vérifiant si la partie est active (est en cours)
jeu_actif = False

    # Booléens vérifiant si le personnage (P1 ou P2) est en train d'attaquer
en_cours_attaqueP1 = False
en_cours_attaqueP2 = False

    # Dernier sprite chargé de chaque personnage
sprite_a_chargerP1 = imagesDroiteP1[0]
sprite_a_chargerP2 = imagesGaucheP2[0]

    # Valeurs des vies des personnages
vie_p1 = VIE_MAX
vie_p2 = VIE_MAX

    # Valeurs des points des personnages
point_p1 = 0
point_p2 = 0

    # Pseudos (avec valeur par défaut) des joueurs
pseudo_j1 = "Joueur 1"
pseudo_j2 = "Joueur 2"

# Création de l'interface du menu
    # Chargement des images correspondantes
image_fond      = PhotoImage(file="img/decor/fond.gif")
image_fond_menu = PhotoImage(file="img/decor/menu.gif")
image_sol       = PhotoImage(file="img/decor/sol.gif")

    # Affichage du menu d'accueil
afficher_menu_accueil()

# Gestion des événements
touches = []
fenetre.bind_all("<KeyPress>", clavier)
fenetre.bind_all("<KeyRelease>", clavier_relachement)
fenetre.bind_all("<Button-1>", souris)

# Boucle principale
fenetre.mainloop()
