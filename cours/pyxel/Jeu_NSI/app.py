import pyxel
import random

"""
Jeu 1
"""

class Jeu_Er:
    def __init__(self):
        pyxel.camera(La_kk_venture.Camera_Buttons,0)
        #==============================
        #Jeu
        #==============================

        # (origine des positions : bas centre)
        self.kk_x = 192  # position initiale du kk en x
        self.kk_y = 112  # position initiale du kk en y
        self.vspd = 0
        self.isgrounded = False
        self.vitesse = 0 # vitesse dash
        self.dash = False #entrain de dash
        self.dash_redy = True #couldown du dash


        # vies
        self.vies = 4

        # sens du joueur
        self.sens = 1

        #est entrain de bouger
        self.inmoove = False

        #gère le profile du personnage lors de son mouvement (animation de marche)
        self.profile_mouvement = 0

        #accroupi ou non
        #boolean gérant si le perso peu ou non etre shield
        self.accroupi = False
        self.peut_shield = True


        # score
        self.score = 0

        # compteur temps
        #et variable d'appariton de bombe en fonction du temps (changer la valeur initiale en fonction de la durré de la partie *1200 chaud vers 1"25' crash au bout d'environ 3"20',score moyen atteind 60*)
        self.temps = 0
        self.tbommbe = 1200


        # initialisation des fruits
        self.fruit_liste = []

        # initialisation des ennemis
        self.ennemis_liste = []

        #liste des nuages
        self.nuages_liste = []

        # initialisation des explosions
        self.explosions_liste = []

        # initialisation des explosions aux sol
        self.explosions_liste_sol = []

        # initialisation des fruit aux sol
        self.fruit_liste_sol = []

        # initialisation des animation des fruit récupérées
        self.fruit_recupere = []

        #animation shield
        self.animation_shield = []

        #animation couldown dash
        self.tab_couldown_dash = []

        #animation couldown accrupissement
        self.tab_couldown_shield = [[0,0]] #[valeur du chargement entre 0 et 30, si la 1ére va leur vaut 30 ici va udra 1 (gestion de la couleur en 11 et 12(plein et le chargement))]

        #liste des x et du y des plaformes sous la forme [ x debut , x fin , y (hauteure subjective, visuel) , largeure (de calcule par raport au personnage +8)]
        self.liste_plat= [[0,24,96,8],[48,80,72,8],[104,128,96,8],[0,128,120,8]]

        # initialise la cinematique
        self.Cinematique = -1 # -1 ecrant de chargement / 0 le jeu / -1 la prés face / 2 le post game

        self.proch = 0
        self.dialogue = 0
        self.in_dialogue = False
        self.text = 0
        self.time_out = True
        self.portail = 96
        self.i = 0

        # chargement des images
        pyxel.load("res_E.pyxres")

        #MUUUSIC
        pyxel.playm(0,0,True)

    # compte les secondes et diminue par 2 le generateur de bombe toute les 20 secondes
    def compteur_temps_Er(self):
        if (pyxel.frame_count % 30 == 0) and self.vies > 0 and self.score < 60 and self.Cinematique == 0 :
            self.temps += 1
        if (pyxel.frame_count % 600 == 0):
            self.tbommbe = self.tbommbe // 2

    def joueur_Er(self):
        '''acroupi ou non '''

        if self.kk_y < 149 and self.kk_y > 112 :
            self.kk_y = 112


        if La_kk_venture.Down : # flèche bas pressée

            if self.kk_y != 112 : #si il est pas au sol (sur un eplatforme) il descent
                self.kk_y +=8
                self.isgrounded = False


            if self.peut_shield : # si il peut activer son shield
                for shield in self.tab_couldown_shield :
                    if shield[0] <= 0 :
                        self.peut_shield = False
                        shield[0] = 0
                    else :
                        shield[0] -= 0.2

            self.accroupi = True # il est accroupi

        else : # la touche n'est pas pressée , il n'est pas accroupis
            self.accroupi = False


        """déplacement avec les touches de directions"""
        if La_kk_venture.Right and self.kk_x < 120 and not(self.accroupi):#not(self.accroupi) ------> le kk n'est pas accroupi
            self.kk_x += 2
            self.sens = 1

        if La_kk_venture.Left and self.kk_x > 0 and not(self.accroupi):
            self.kk_x += -2
            self.sens = -1

        if La_kk_venture.Left or La_kk_venture.Right :
            self.inmoove = True
        else:
            self.inmoove = False


        '''dash'''
        if La_kk_venture.Space and not(self.accroupi) and self.dash_redy: #Si ESPACE appuyer
            self.vitesse = self.sens*7 #Taille du dash
            self.dash_redy = False
            self.tab_couldown_dash.append([0])

        #Gravité du dash
        if round(self.vitesse) != 0 :
            self.vitesse = min(6, self.vitesse + 1*(-(self.sens))) #Argument1 : Vitesse maximale, Argument2 : Accélération
            self.dash = True
        else:
            self.dash = False
        if self.accroupi or self.kk_x <= 4 or self.kk_x >= 120:
            self.vitesse = 0
            self.dash = False

        self.kk_x += self.vitesse

        '''MERCI LE KD'''
        #Saut
        if La_kk_venture.Up_p and self.isgrounded and not(self.accroupi): #Si ESPACE appuyer
            self.vspd = -8 #Taille du saut

        #Gravité
        self.vspd = min(6, self.vspd + 0.90) #Argument1 : Vitesse maximale, Argument2 : Accélération

        #Collision au sol gérer par sur_plat

        self.kk_y += self.vspd

     #teste si le personnage est sur une platfomre et le met au sol

    def sur_plat_Er(self):
        for plat in self.liste_plat:
            if self.kk_y +8 > plat[2]:
                if self.kk_y+8  <= plat[2] +8 and self.kk_x > plat[0]-8 and self.kk_x < plat[1] :
                    self.kk_y = plat[2] -8
                    self.isgrounded = True
                    return True
        self.isgrounded = False

    '''MERCI POUR TOUTE CETTE PARTIE sans la modif pour les platforme , oui j'ai du modifier ton code'''



    def fruit_creation_Er(self):
        """création aléatoire des fruits"""

        # un fruit par 2 secondes
        if (pyxel.frame_count % 60 == 0):
            self.fruit_liste.append([random.randint(0, 120), 0])


    def fruit_deplacement_Er(self):
        """déplacement des fruits vers le bas et suppression s'ils sortent du cadre"""

        for fruit in self.fruit_liste:
            fruit[1] += 1
            if fruit[1] > 116:
                self.fruit_liste.remove(fruit)
                self.fruit_liste_sol.append([fruit[0], fruit[1], 0])

    def ennemis_creation_Er(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % self.tbommbe == 0):
            self.ennemis_liste.append([random.randint(0, 120), 0])

    def ennemis_deplacement_Er(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

        for ennemi in self.ennemis_liste:
            ennemi[1] += 2
            if ennemi[1] > 116:
                self.ennemis_liste.remove(ennemi)
                self.explosions_liste_sol.append([ennemi[0], ennemi[1], 0])

    def compteur_score_Er(self):
        """disparition du fruit et mise a jour du score"""

        for fruit in self.fruit_liste:
            if (
                fruit[0] <= self.kk_x + 8
                and fruit[1] <= self.kk_y + 8
                and fruit[0] + 8 >= self.kk_x
                and fruit[1] + 8 >= self.kk_y
            ):
                self.fruit_liste.remove(fruit)
                self.score += 1
                self.fruit_recupere.append([fruit[0], fruit[1], 0])

    def kk_suppression_Er(self):
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:
            if (
                ennemi[0] <= self.kk_x + 8
                and ennemi[1] <= self.kk_y + 8
                and ennemi[0] + 8 >= self.kk_x
                and ennemi[1] + 8 >= self.kk_y
            ):
                if self.accroupi and self.peut_shield :
                    self.ennemis_liste.remove(ennemi)
                    self.animation_shield.append([self.kk_x, self.kk_y,0])
                else :
                    self.ennemis_liste.remove(ennemi)
                    self.vies -= 1
                    # on ajoute l'explosion
                    self.explosions_creation_Er(self.kk_x, self.kk_y)

    def explosions_creation_Er(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])

    # bombe sur le joueur
    def explosions_animation_Er(self):
        """animation des explosions dans ta gueule"""
        for explosion in self.explosions_liste:
            explosion[2] += 1
            if explosion[2] == 6:
                pyxel.play(2,5)
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    # bombe sur le sol
    def explosions_animation_sol_Er(self):
        """animation des explosions aux sol"""
        for explosion in self.explosions_liste_sol:
            explosion[2] += 1
            if explosion[2] == 8:
                pyxel.play(1,3)
            if explosion[2] == 16:
                self.explosions_liste_sol.remove(explosion)

    # fruit au sol
    def fruit_sol_Er(self):
        """animation des fruit perdu"""
        for fruit in self.fruit_liste_sol:
            fruit[2] += 1
            if fruit[2] == 8:
                self.fruit_liste_sol.remove(fruit)

    def fruit_pris_Er(self):
        """animation des fruit pris"""
        for fruit in self.fruit_recupere:
            fruit[2] += 1
            if fruit[2] == 4:
                pyxel.play(1,4)
            if fruit[2] == 8:
                self.fruit_recupere.remove(fruit)

    def anim_shield_Er (self):
        for bomb in self.animation_shield:
            bomb[2] += 1
            if bomb[2] == 8:
                pyxel.play(1,6)
            if bomb[2] == 14:
                self.animation_shield.remove(bomb)

    def couldown_dash_Er(self):
        for anim in self.tab_couldown_dash:
            anim[0] += 1
            if anim[0] == 30:
                self.tab_couldown_dash.remove(anim)
                self.dash_redy = True

    def couldown_shield_Er(self):
        if not self.accroupi :
            for shield in self.tab_couldown_shield:
                if shield[0] >= 30:
                    self.peut_shield = True
                    shield [0] = 30
                    shield[1] = 1
                else :
                    shield[1] = 0
                    self.peut_shield = False
                    shield[0] += 0.2

    def animation_mouvement_Er (self):
        if (pyxel.frame_count % 5 == 0) :
            if self.profile_mouvement == 0 :
                self.profile_mouvement = 8
            else :
                self.profile_mouvement = 0


    def nuage_creation_Er (self):
        x = random.randint(1,5) # variable de creation de nuage (5 nuages différents)
        if (pyxel.frame_count % 15 == 0) : #creation 1 toute les deux secondes
            #self.nuages_liste.append([0,random.randint(0,112),0,0,0,0]) = (son x(evolutif), son y(evolutif), le x de son dessin , le y de son dessin, longeur du dessin , hauteur du dessin , sa vitesse)
            if x == 1 :
                self.nuages_liste.append([0,random.randint(0,112),32,0,8,8,0.5])
            elif x == 2 :
                self.nuages_liste.append([0,random.randint(0,112),40,0,8,8,1])
            elif x == 3 :
                self.nuages_liste.append([0,random.randint(0,112),48,8,8,8,1])
            elif x == 4 :
                self.nuages_liste.append([0,random.randint(0,112),56,8,8,8,0.5])
            else : # x == 5 :
                self.nuages_liste.append([0,random.randint(0,112),32,8,16,16,0.2])
        for nuage in self.nuages_liste :
            nuage[0] += nuage[6]
            if nuage [0] == 128:
                self.nuages_liste.remove(nuage)


    def stop_Er(self):
            self.kk_y = 112
            self.kk_x = 64
            self.fruit_liste = []
            self.ennemis_liste = []
            self.explosions_liste = []
            self.explosions_liste_sol = []
            self.fruit_liste_sol = []
            self.fruit_recupere = []

    def reboot_Er (self):
        self.kk_x = 60 # position initiale du kk en x
        self.kk_y = 112  # position initiale du kk en y
        self.vspd = 0
        self.isgrounded = False
        self.vitesse = 0 # vitesse dash
        self.dash = False #entrain de dash
        self.dash_redy = True #couldown du dash
        self.vies = 4
        self.sens = 1
        self.inmoove = False
        self.profile_mouvement = 0
        self.accroupi = False
        self.peut_shield = True
        self.score = 0
        self.temps = 0
        self.tbommbe = 1200
        self.tab_couldown_shield = [[0,0]]
        self.liste_plat= [[0,24,96,8],[48,80,72,8],[104,128,96,8],[0,128,120,8]]
        self.Cinematique = 0
    #==================================
    #Cinematique
    #==================================
    def joueur_cinametique_Er (self):

        if self.kk_y < 149 and self.kk_y > 112 :
            self.kk_y = 112

        if La_kk_venture.Right and self.kk_x < 248 and not(self.accroupi):#not(self.accroupi) ------> le kk n'est pas accroupi
            self.kk_x += 2
            self.sens = 1

        if La_kk_venture.Left and self.kk_x > 128 and not(self.accroupi):
            self.kk_x += -2
            self.sens = -1

        if La_kk_venture.Left or La_kk_venture.Right :
            self.inmoove = True
        else:
            self.inmoove = False

        if La_kk_venture.Up and self.isgrounded and not(self.accroupi): #Si ESPACE appuyer
            self.vspd = -8 #Taille du saut

        #Gravité
        if not self.isgrounded :
            self.vspd = min(6, self.vspd + 0.9) #Argument1 : Vitesse maximale, Argument2 : Accélération

        #Collision au sol gérer par sur_plat

        self.kk_y += self.vspd

        if La_kk_venture.Down : # flèche bas pressée
            self.accroupi = True # il est accroupi

        else : # la touche n'est pas pressée , il n'est pas accroupis
            self.accroupi = False

    def sur_plat_cine_Er (self):
        if self.kk_y +8 >= 120:
            if self.kk_y+8  <= 120 +8  :
                self.kk_y = 112
                self.isgrounded = True
                return True
        self.isgrounded = False

    def proche_Er (self):
        if 128 < self.kk_x < 148 and self.Cinematique == 1 :
            if self.dialogue == 1 :
                self.proch = 2
                if La_kk_venture.F :
                    self.dialogue = 2
                    self.in_dialogue = True
        elif self.kk_x >= 240 and self.Cinematique == 1 :
            if self.dialogue == 0 :
                self.proch = 1
                if La_kk_venture.F :
                    self.dialogue = 1
                    self.in_dialogue = True
                    self.text = 1
        elif 128 < self.kk_x < 148 and self.Cinematique == 2 :
            if self.dialogue == 2 :
                self.proch = 2
                if La_kk_venture.F :
                    self.dialogue = 3
                    self.in_dialogue = True
        else :
            self.proch = 0

    def anim_dialogue_Er (self):
        if self.in_dialogue == True and self.time_out :
            #Aiaria
            if self.dialogue == 1 :
                La_kk_venture.Choix = True #Afficher les touches A et B
                if self.text == 1:
                    if La_kk_venture.A_p: #non
                        self.text = 0
                        self.dialogue = 0
                        self.time_out = False
                        self.in_dialogue = False
                    elif La_kk_venture.B_p: #oui
                        self.time_out = False
                        self.text = 2
                elif self.text == 2:
                    if La_kk_venture.A_p:# refuser la quéte
                        self.Cinematique = 666
                        self.in_dialogue = False
                    elif La_kk_venture.B_p: #acépter la quéte
                        self.text = 4
                        self.time_out = False
                elif self.text == 4:
                    if La_kk_venture.A_p:# quité le dialogue
                        self.text = 1
                        self.dialogue = 1
                        self.time_out = False
                        self.in_dialogue = False
            #Kara prés face
            elif self.dialogue == 2 :
                La_kk_venture.Choix = True #Afficher les touches A et B
                if self.text == 1:
                    if La_kk_venture.A_p: # refusé
                        self.Cinematique = 667
                        self.time_out = False
                        self.in_dialogue = False
                    elif La_kk_venture.B_p: #oui
                        self.text = 2
                        self.time_out = False
                elif self.text == 2 :
                    if La_kk_venture.A_p: #ok
                        self.text = 3
                        self.time_out = False
                elif self.text == 3 :
                    if La_kk_venture.A_p: #ok
                        self.kk_y =112
                        self.in_dialogue = False
                        self.Cinematique = 100
                        self.time_out = False
                        self.text = 1
                        self.dialogue = 2
            #kara post game
            elif self.dialogue == 3 :
                La_kk_venture.Choix = True #Afficher les touches A et B
                if self.text == 1: #donner les pommes
                    if La_kk_venture.A_p: #non
                        self.text = 1
                        self.dialogue = 2
                        self.time_out = False
                        self.in_dialogue = False
                    elif La_kk_venture.B_p: #oui
                        self.time_out = False
                        self.text = 2
                elif self.text == 2 : # eplication 1
                    if La_kk_venture.A_p: #ok
                        self.text = 3
                        self.time_out = False
                elif self.text == 3 : # eplication 1
                    if La_kk_venture.A_p: #ok
                        self.text = 4
                        self.time_out = False
                elif self.text == 4 : #pret ???
                    if La_kk_venture.A_p: #non
                        self.text = 1
                        self.dialogue = 2
                        self.time_out = False
                        self.in_dialogue = False
                    elif La_kk_venture.B_p: #oui
                        self.in_dialogue = False
                        self.Cinematique = 3
                        self.time_out = False
                        self.text = 1
                        self.dialogue = 3
                        self.kk_x = 128+64

    def varriateur_Er (self):
        if pyxel.frame_count % 20 == 0:
            if self.portail == 96:
                self.portail = 112
            else :#self.portail == 112:
                self.portail = 96
            if self.i == 4:
                self.Cinematique = -2
                La_kk_venture.Jeu = 2
                La_kk_venture.Initialisation = True
                pyxel.stop()
            else :
                self.i += 1

    #=======
    def ver_jeu_Er (self):
        if self.Cinematique == 100 :
            if self.kk_x == 0 :
                self.Cinematique = 0
                self.kk_x = 64
            else :
                self.kk_x -= 1
                self.inmoove = True
                self.sens = -1
        elif self.Cinematique == -100 :
            if self.kk_x == 129 :
                self.Cinematique = 2
                self.kk_x = 129
            else :
                self.kk_x += 1
                self.inmoove = True
                self.sens = 1

    #=====
    def debug_Er(self):
        # if pyxel.btn(pyxel.KEY_L) :
        #     self.reboot_Er()
        #     self.Cinematique = int(input("cinematique"))
        # if pyxel.btn(pyxel.KEY_V):
        #     self.vies = int(input("vies"))
        # if pyxel.btn(pyxel.KEY_P):
        #     self.score = int(input("score"))
        if self.time_out == False :
            if pyxel.frame_count % 30 == 0 :
                self.time_out = True

    #================================
    #prés face
    #================================


    def lunch_Er (self):
        if La_kk_venture.Space :
            self.Cinematique = 1
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.Cinematique = 1
            La_kk_venture.On_Mobile = True


    def update(self):
        self.debug_Er()
        if self.Cinematique == 0 :

            # compteur temps
            self.compteur_temps_Er()

            # deplacement du vaisseau
            self.joueur_Er()

            # creation des fruit
            self.fruit_creation_Er()

            # mise a jour des positions des fruits
            self.fruit_deplacement_Er()

            # creation des ennemis
            self.ennemis_creation_Er()

            # mise a jour des positions des ennemis
            self.ennemis_deplacement_Er()

            # mise a jour du score et de la position des fruits
            self.compteur_score_Er()

            # suppression du vaisseau et ennemi si contact
            self.kk_suppression_Er()

            # evolution de l'animation des explosions
            self.explosions_animation_Er()

            # explosion au sol
            self.explosions_animation_sol_Er()

            # fruit aux sol
            self.fruit_sol_Er()

            # fruit récupérée
            self.fruit_pris_Er()

            #effet bombe sur shield
            self.anim_shield_Er ()

            #gère le rechargement du dash
            self.couldown_dash_Er ()

            #gère le rechargement du shield
            self.couldown_shield_Er ()

            #vérifi si le caca est su rune paltforme ou dans le vide (remplace la gravitée)
            self.sur_plat_Er ()

            #change profile_mouvement pour avoir une animation
            self.animation_mouvement_Er ()

            #gére l'aparition la supretion et le mouvement des nuages
            self.nuage_creation_Er ()

        elif self.Cinematique == 1 :

            self.nuage_creation_Er ()

            self.animation_mouvement_Er ()

            self.proche_Er ()

            #position du jouer (fait bouger la tilemap)
            if not self.in_dialogue  :
                self.joueur_cinametique_Er ()

            self.sur_plat_cine_Er()

            self.anim_dialogue_Er ()


        elif self.Cinematique == 100 :

            self.nuage_creation_Er ()

            self.ver_jeu_Er ()

            self.animation_mouvement_Er ()

        elif self.Cinematique == -100 :

            self.nuage_creation_Er ()

            self.ver_jeu_Er ()

            self.animation_mouvement_Er ()

        elif self.Cinematique == -1 :

            #gére l'aparition la supretion et le mouvement des nuages
            self.nuage_creation_Er ()

            #si espace appuyé commencé la cinématique
            self.lunch_Er ()

        elif self.Cinematique == 2 :

            self.nuage_creation_Er ()

            self.animation_mouvement_Er ()

            self.proche_Er ()

            #position du jouer (fait bouger la tilemap)
            if not self.in_dialogue  :
                self.joueur_cinametique_Er ()

            self.sur_plat_cine_Er()

            self.anim_dialogue_Er ()

        elif self.Cinematique == 3:
            self.nuage_creation_Er ()

            self.varriateur_Er()

        elif self.Cinematique == 666 :
            self.nuage_creation_Er ()

    def draw(self):
        # vide la fenetre
        pyxel.cls(0)

        if self.Cinematique == 0 :

            # si le caca possede des vies le jeu continue et que le score est inferieur a 60
            if self.vies > 0 and self.score < 10 :

                #affiche le ciel
                pyxel.bltm(0, 0, 1, 0, 0, 128, 128)

                #affiche les nuages
                for nuage in self.nuages_liste:
                    pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)

                # affiche les platformes
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128,0)

                # affichage des vies
                if self.vies == 4 :
                    pyxel.blt(8, 0 , 0, 56, 32, 24, 16, 0)
                elif self.vies == 3 :
                    pyxel.blt(8, 0 , 0, 16, 32, 16, 16, 0)
                elif self.vies == 2 :
                    pyxel.blt(8, 0 , 0, 32, 32, 16, 16, 0)
                else :
                    pyxel.blt(8, 0 , 0,48, 32, 8, 16, 0)

                # affichage du score
                pyxel.text(50, 6, str(self.score) + "/ 10", 0)

                # affiche le temps en minute - seconde
                pyxel.text(97, 6, str(self.temps // 60) + "''" + str(self.temps % 60) + "'", 0)

                #affiche le cooldown du dash
                for anim in self.tab_couldown_dash:
                    pyxel.text(75, 122, "dash", 0)
                    pyxel.rect(95, 121, anim[0] , 6, 10)

                for shield in self.tab_couldown_shield:
                    pyxel.text(1, 122, "shield", 0)
                    pyxel.rect(25, 121, shield[0] , 6, 12 - shield[1] )


                # kk (carre 8x8)
                if not self.accroupi and not self.dash: #ne dash pas et n'est pas accroupi
                    if self.inmoove :
                        pyxel.blt(self.kk_x, self.kk_y, 0, self.profile_mouvement, 32, (self.sens * 8), 8, 0)
                    else : #n'est pas en mouvement
                        pyxel.blt(self.kk_x, self.kk_y, 0, 0, 0, (self.sens * 8), 8, 0)
                elif  self.dash: #le caca dash
                    pyxel.blt(self.kk_x, self.kk_y, 0, 16, 8, (self.sens * (-8)), 8, 0) #-8 car dessin a l'enver
                else : # le kk est accroupi
                    pyxel.blt(self.kk_x, self.kk_y, 0, 8, 8, (self.sens * 8), 8, 0)
                    if self.peut_shield : #le caca peut shield
                        pyxel.circb(self.kk_x+4, self.kk_y+4, 5, 6)
                        pyxel.circb(self.kk_x+4, self.kk_y+4, 6, 5)

                # fruits
                for fruit in self.fruit_liste:
                    pyxel.blt(fruit[0], fruit[1], 0, 8, 0, 8, 8, 0)

                # ennemis
                for ennemi in self.ennemis_liste:
                    pyxel.blt(ennemi[0], ennemi[1], 0, 0, 40, 8, 8, 12)

                # explosions (cercles de plus en plus grands)
                for explosion in self.explosions_liste:
                    pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)

                for explosion in self.explosions_liste_sol:
                    pyxel.circ(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)

                for bomb in self.animation_shield:
                    pyxel.circ(self.kk_x + 4, self.kk_y + 4, 2 * (bomb[2] // 4),5 + bomb[2] % 2)

                for fruit in self.fruit_liste_sol:
                    pyxel.circ(fruit[0] + 4, fruit[1] + 4, 2 * (fruit[2] // 4), 8)

                for fruit in self.fruit_recupere:
                    pyxel.circ(fruit[0] + 4, fruit[1] + 4, 2 * (fruit[2] // 4), 10 + fruit[2] % 2)

            elif self.score >= 10 :
                #affiche le ciel
                pyxel.bltm(0, 0, 1, 0, 0, 128, 128)

                #affiche les nuages
                for nuage in self.nuages_liste:
                    pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)

                # affiche les platformes
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128,0)

                #le kk
                pyxel.blt(self.kk_x, self.kk_y, 0, 0, 0, (self.sens * 8), 8, 0)

                # ecrant de passage
                pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)


                pyxel.text(5, 38, "Vive la NSI \ntu peux choisir avec toutes \nles autres spe. ", 0)
                pyxel.text(32, 48, "LIFE: " + str(self.vies), 0)
                pyxel.text(32, 58, "TIME: " + str(self.temps // 60) + ";" + str(self.temps % 60), 0)
                pyxel.text(52, 112 ,f"suite"  , 0)
                La_kk_venture.Choix = True #Afficher touche A et B
                self.stop_Er ()
                if La_kk_venture.A :
                    self.kk_x = 64
                    self.Cinematique = -100


            # sinon: GAME OVER
            else :
                pyxel.bltm(0, 0, 0, 3*128, 0, 128, 128)
                pyxel.text(5, 64, "Pret a choisir le spe NSI ? \nOn peut meme la choisir sans \nles Maths.", 0)
                pyxel.text(32, 78, "SCORE:" + str(self.score), 0)
                pyxel.text(32, 84, "TEMPS:" + str(self.temps // 60) + ";" + str(self.temps % 60), 0)
                pyxel.text(15, 94, "presser F pour recommencer", 0)
                La_kk_venture.Press_F = True #Afficher touche F
                self.stop_Er()
                if La_kk_venture.F :
                    self.reboot_Er()

        elif self.Cinematique == 1 or self.Cinematique == 100 or self.Cinematique == -100 or self.Cinematique == 2:

            #affiche le ciel
            pyxel.bltm(0, 0, 1, 0, 0, 128, 128)

            #affiche les nuages
            for nuage in self.nuages_liste:
                pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)

            #murail
            pyxel.bltm(0, 0, 1, 128, 0, 128, 128,12)

            # affiche le fond
            pyxel.bltm(0, 0, 0, self.kk_x, 128, 128, 128,9)

            if  self.accroupi == False and not self.in_dialogue :
                if self.inmoove :
                    pyxel.blt(64, self.kk_y, 0, self.profile_mouvement, 32, (self.sens * 8), 8, 0)
                else : #n'est pas en mouvement
                    pyxel.blt(64, self.kk_y, 0, 0, 0, (self.sens * 8), 8, 0)
            elif not self.in_dialogue : # le kk est accroupi
                pyxel.blt(64, self.kk_y, 0, 8, 8, (self.sens * 8), 8, 0)

            if self.proch == 2 and not self.in_dialogue and self.Cinematique != 100 and self.Cinematique != -100: #kara
                pyxel.text(64 , 64 , "F pour parler",0)
                La_kk_venture.Press_F = True #Afficher touche F
            elif self.proch == 1 and not self.dialogue and self.Cinematique != 100 and self.Cinematique != -100: # iria
                pyxel.text(64 , 64 , "F pour parler",0)
                La_kk_venture.Press_F = True #Afficher touche F

            if self.in_dialogue :
                if self.dialogue == 1:
                    if self.text == 1 :
                        pyxel.bltm(0, 0, 2, 0, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f" Hey \nj'ai une quete \npour toi \nVeux-tu tester la \nspe NSI ??"  , 0)
                        pyxel.text(20, 112 ,f" NON   "  , 0)
                        pyxel.text(92, 112 ,f" OUI   "  , 0)
                    if self.text == 2 :
                        pyxel.bltm(0, 0, 2, 0, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Un monstre aux\nalures de \nchauves-souris \nrode !\nVa le tuer !! "  , 0)
                        pyxel.text(20, 112 ,f" NON   "  , 0)
                        pyxel.text(92, 112 ,f" OUI   "  , 0)
                    if self.text == 4 :
                        pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Va voir Kara \nla sorciere elle \npourra t'aider à faire \nUne première spe NSI.   "  , 0)
                        pyxel.text(64, 112 ,f" OK  "  , 0)
                if self.dialogue == 2:
                    if self.text == 1 :
                        pyxel.bltm(0, 0, 2, 0, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f" Salut \nJe peux t'offrir \nmon aide si \ntu vas me chercher \n10 pommes\n"  , 0)
                        pyxel.text(20, 112 ,f" NON   "  , 0)
                        pyxel.text(92, 112 ,f" OK   "  , 0)
                    if self.text == 2 :
                        pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Bien \npour t'aider \nje vais t'offrir \ndes pouvoirs \n-un bouclier avec \n la fleche du bas "  , 0)
                        pyxel.text(64, 112 ,f" OK   "  , 0)
                    if self.text == 3 :
                        pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"ET \n- un dash avec \nla barre espace \n\nils te seront \nutiles prend garde\na leur systeme de \nrecharge  "  , 0)
                        pyxel.text(64, 112 ,f" OK   "  , 0)
                if self.dialogue == 3:
                    if self.text == 1 :
                        pyxel.bltm(0, 0, 2, 0, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Alors !? \nAs-tu trouve \nces pommes ? \nNSI peut etre choisie \navec toutes les autres \nspe."  , 0)
                        pyxel.text(20, 112 ,f" NON   "  , 0)
                        pyxel.text(92, 112 ,f" OUI   "  , 0)
                    if self.text == 2 :
                        pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)
                        pyxel.text(28, 38 ,f"Merci.\nJe vais t'envoyer\nen première \nNSI. Mais sache \nque PYTHON \net la programmation \nseront tes \namis... "  , 0)
                        pyxel.text(64, 112 ,f" ??   "  , 0)
                    if self.text == 3 :
                        pyxel.bltm(0, 0, 2, 128, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Alors, choisis-tu \nla spe NSI ? \nQuel metier souhaites-tu \nfaire ? \nIl y a de grandes\nchances d'avoir besoin\n de l'informatique\n!!"  , 0)
                        pyxel.text(64, 112 ,f" OK   "  , 0)
                    if self.text == 4 :
                        pyxel.bltm(0, 0, 2, 0, 0, 128, 128,9)
                        pyxel.text(32, 38 ,f"Alors .\nPret pour la \nspe NSI ?!! "  , 0)
                        pyxel.text(20, 112 ,f" NON   "  , 0)
                        pyxel.text(92, 112 ,f" OUI   "  , 0)



        elif self.Cinematique == -1 : #ecran d'entré

            #affiche le ciel
            pyxel.bltm(0, 0, 1, 128, 0, 128, 128)

            #affiche les nuages
            for nuage in self.nuages_liste:
                pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)


            # affiche le fond
            pyxel.bltm(0, 0, 0, 256, 0, 128, 128,0)

            pyxel.text(35, 29, "LA NSI-VENTURE ", 0)
            pyxel.text(2, 40, "realise par des eleves de NSI\nL'info : la garantie d'emploi\nAvec toutes les autres spe\nEt meme sans choisir les Maths\nDans tous les metiers\nOn a besoin de NSI\nMedecine Banque Production Vente ect...", 0)
            pyxel.text(20, 116, "espace pour jouer ", 0)
            pyxel.text(2, 122, "la NSI + toutes les spe OK! ", 0)


        elif self.Cinematique == 3:

            #murail + ciel
            pyxel.bltm(0, 0, 1, 128, 0, 128, 128)

            #affiche les nuages
            for nuage in self.nuages_liste:
                pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)

            # affiche le fond
            pyxel.bltm(0, 0, 0, 128, 128, 128, 128,9)

            pyxel.blt(64, 112, 0, 0, 0, (self.sens * 8), 8, 0)
            pyxel.blt(64, self.kk_y - 16, 0, self.portail, 48, 16, 32,9)


        elif self.Cinematique >= 666 :
            if self.Cinematique == 666 :
                pyxel.bltm(0, 0, 1, 128, 0, 128, 128)

                #affiche les nuages
                for nuage in self.nuages_liste:
                    pyxel.blt(nuage[0], nuage[1],0, nuage[2], nuage[3], nuage[4], nuage[5], 12)

                # affiche le fond
                pyxel.bltm(0, 0, 0, 256, 0, 128, 128,0)

                # affiche le fond
                pyxel.bltm(0, 0, 0, 256, 0, 128, 128,0)
                pyxel.text(2, 29, "La NSI peut se choisir ", 0)
                pyxel.text(3, 122, "avec toutes les autres spé", 0)
            elif self.Cinematique == 667:
                pyxel.bltm(0, 0, 0, 3*128, 0, 128, 128)

                pyxel.text(55, 64, "GAME OVER", 0)
                pyxel.text(8, 52, "Pret à choisir NSI !", 0)
                pyxel.text(30, 70, "avec ou sans les Maths,\n et toutes les autres spe !!", 0)
                pyxel.text(30, 100, "Informatique: garantie d'emploi", 0)
        elif self.Cinematique == -2 :
            pyxel.cls(12)


"""
Jeu 2
"""

class Jeu_D:
    def __init__(self):
        pyxel.camera(0,0)
        self.x = 30
        self.y = 112
        self.hspd = 0
        self.vspd = 0
        self.speed = 2
        self.Tap_Orb = False
        self.size = 8
        self.isgrounded = False
        self.rotate = 0
        self.xcam = 0
        self.ycam = 0
        self.Backgrounds_liste = []
        self.Tile_Sol = [(3,1),(4,1),(5,1),(6,1),(3,3),(4,3),(5,3),(6,3),(4,0),(2,1),(2,3)]
        self.Tile_Kill = [(4,0), (9,2),(10,2),(11,2),(9,3),(10,3),(11,3),(9,4),(10,4),(11,4), (13,3),(14,2),(14,3),(14,4),(15,3),(12,6),(14,6), (4,6),(5,6),(6,6),(7,6),(6,7),(7,7)] #Bloc Kill / Piques
        self.Tile_Color_Kill = [(8,4), (8,5),(9,5),(10,5),(11,5), (8,6),(9,6),(10,6),(11,6), (8,7),(9,7),(10,7),(11,7), (9,8),(10,8)] #All Colors
        self.Port_Cube = [(0,5),(0,6),(0,7)]
        self.Port_Ball = [(0,2),(0,3), (0,4)]
        self.Port_Wave = [(1,2),(1,3),(1,4)]
        self.Tile_Port_Speed_Blue = [(0,8),(1,8),(0,9),(1,9)]
        self.Tile_Port_Speed_Green = [(2,8),(3,8),(2,9),(3,9)]
        self.Tile_Port_Speed_Red = [(4,8),(5,8),(4,9),(5,9),(6,8),(6,9)]
        self.Wave_trail_cords = [[0,0],[0,0]]
        self.Wave_Trail_Draw = []
        self.Circle_list = [] #Argument : [x,y,rayon,couleur]
        self.Circle_list_out = [] #Argument : [x,y,rayon = 0,couleur]
        self.Tile_Type_Collision = () #Argument : (a, b)
        self.Coin_count = 0
        self.Coin_max = 10
        self.Pixel_Dust_liste = [] #Argument : [x,y,mod_y,timer]
        self.Level_Count = 0
        self.Level_Previous = self.Level_Count
        self.Attemps_Count = 0
        self.Start_x = 30
        self.Start_y = 112
        self.isdead = False
        self.Death_Chrono = 30
        self.Starting_Screen = True

        #Bouton
        self.Space = pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
        self.Space_p = pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

        #Mode
        self.Mode = 0 #0 = Cube ; 1 = Ball ; 2 = Wave
        #Ball
        self.Gravity = 1 #1 = Gravité normal ; -1 = Gravité inversée

        #Cinématique
        self.Cin_begin = True
        self.Cin_end = 0
        self.Cin_Chrono = 300
        self.Cin_fin_Chrono = 100
        self.infall = False
        self.end_of_game = False

        pyxel.load("res_D.pyxres")

    def Collision_y_D(self):
        if self.vspd > 0: #Sprite Bas
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x) + self.hspd)//8, ((self.y+self.size)+1)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x+8) + self.hspd)//8, ((self.y+self.size)+1)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
        else: #Sprite Haut
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x) + self.hspd)//8, ((self.y)-1)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x+8) + self.hspd)//8, ((self.y)-1)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
        return False

    def Collision_Speed_D(self):
        if self.vspd > 0: #Sprite Bas
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x) + self.hspd)//8, ((self.y+self.size) + self.vspd)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x+8) + self.hspd)//8, ((self.y+self.size) + self.vspd)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
        else: #Sprite Haut
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x) + self.hspd)//8, ((self.y) + self.vspd)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
            self.Tile_Type_Collision = pyxel.tilemap(4).pget(((self.x+8) + self.hspd)//8, ((self.y) + self.vspd)//8) #Optimisation, évite des calculs de tuiles non utile
            for Sol in self.Tile_Sol:
                if self.Tile_Type_Collision == Sol:
                    return True
        return False

    def Collision_death_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8) #Optimisation, évite des calculs de tuiles non utile
        for Death in self.Tile_Kill:
            if self.Tile_Type_Collision == Death:
                return True
        for Death in self.Tile_Color_Kill:
            if self.Tile_Type_Collision == Death:
                return True
        return False

    def Collision_Death_Rampe_D(self):
        self.Tile_Rampe_Gauche = [(7,2),(7,3)]
        self.Tile_Rampe_Droite = [(8,2),(8,3)]
        if pyxel.tilemap(4).pget((self.x)//8, (self.y)//8) == (7,2): #Haut Gauche
            return True
        if pyxel.tilemap(4).pget((self.x)//8, (self.y+self.size)//8) == (7,3): #Bas Gauche
            return True
        if pyxel.tilemap(4).pget((self.x+self.size)//8, (self.y)//8) == (8,2): #Haut Droite
            return True
        if pyxel.tilemap(4).pget((self.x+self.size)//8, (self.y+self.size)//8) == (8,3): #Bas Droite
            return True
        return False


    def Collision_Orb_D(self):
        if pyxel.tilemap(4).pget((self.x)//8, (self.y)//8) == (3,0):
            return True
        if pyxel.tilemap(4).pget((self.x)//8, (self.y+self.size)//8) == (3,0):
            return True
        if pyxel.tilemap(4).pget((self.x+self.size)//8, (self.y)//8) == (3,0):
            return True
        if pyxel.tilemap(4).pget((self.x+self.size)//8, (self.y+self.size)//8) == (3,0):
            return True
        return False

    def Collision_Pad_Yellow_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8)
        if self.Gravity == 1:
            if self.Tile_Type_Collision == (7,8):
                return True
        else:
            if self.Tile_Type_Collision == (7,9):
                return True
        return False
    def Collision_Pad_Blue_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8)
        if self.Gravity == 1:
            if self.Tile_Type_Collision == (8,8):
                return True
        else:
            if self.Tile_Type_Collision == (8,9):
                return True
        return False

    def Collision_Coin_D(self):
        if pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8) == (2,0):
            pyxel.tilemap(4).pset((self.x+self.size/2)//8, (self.y+self.size/2)//8, (1,1))
            self.Coin_count += 1
            return True
        return False

    #Collision portal speed
    def Collision_Port_Speed_Blue_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8)
        for Col in self.Tile_Port_Speed_Blue:
            if self.Tile_Type_Collision == Col:
                if self.speed != 2:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,12])
                    self.speed = 2
                return True
        return False
    def Collision_Port_Speed_Green_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8)
        for Col in self.Tile_Port_Speed_Green:
            if self.Tile_Type_Collision == Col:
                if self.speed != 3:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,11])
                    self.speed = 3
                return True
        return False
    def Collision_Port_Speed_Red_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+self.size/2)//8, (self.y+self.size/2)//8)
        for Col in self.Tile_Port_Speed_Red:
            if self.Tile_Type_Collision == Col:
                if self.speed != 4:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,8])
                    self.speed = 4
                return True
        return False


    def Collision_Port_Cube_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+4)//8, (self.y+4)//8) #Optimisation, évite des calculs de tuiles non utile
        for Col in self.Port_Cube:
            if self.Tile_Type_Collision == Col:
                if self.Mode != 0:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,11])
                self.Mode = 0
                self.size = 8 #Taille
                return True
        return False

    def Collision_Port_Ball_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+4)//8, (self.y+4)//8) #Optimisation, évite des calculs de tuiles non utile
        for Col in self.Port_Ball:
            if self.Tile_Type_Collision == Col:
                if self.Mode != 1:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,9])
                self.Mode = 1
                self.size = 8 #Taille
                return True
        return False

    def Collision_Port_Wave_D(self):
        self.Tile_Type_Collision = pyxel.tilemap(4).pget((self.x+4)//8, (self.y+4)//8) #Optimisation, évite des calculs de tuiles non utile
        for Col in self.Port_Wave:
            if self.Tile_Type_Collision == Col:
                if self.Mode != 2:
                    self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,6])
                self.Mode = 2
                self.size = 6 #Taille
                self.Gravity = 1
                self.Wave_Trail_Draw = []
                return True
        return False

    def Pixel_Dust_D(self):
        for pixel in self.Pixel_Dust_liste:
            pixel[0] -= 0
            pixel[1] -= pixel[2]
            pixel[3] -= 1
            if pixel[3] == 0:
                self.Pixel_Dust_liste.remove(pixel)


    #Joueur
    def Cube_D(self):
        #Avancé vers l'avant
        self.hspd = self.speed

        #Saut
        if (self.Space) and self.isgrounded == True and self.Cin_end == False: #Si ESPACE appuyer
            self.vspd = -6*self.Gravity #Taille du saut

        #Tap une Orb
        if (self.Space_p) and self.isgrounded == False:
            self.Tap_Orb = True
        if self.Tap_Orb == True and not (self.Space):
            self.Tap_Orb = False
        if self.isgrounded == True:
            self.Tap_Orb = False

        #Gravité qui change
        if self.Gravity == 1:
            self.vspd = min(6, self.vspd + 0.90) #Argument1 : Vitesse maximale, Argument2 : Accélération
        else:
            self.vspd = max(-6, self.vspd - 0.90) #Argument1 : Vitesse maximale, Argument2 : Accélération

        #Collison avec une Orb
        if self.Tap_Orb == True and self.Collision_Orb_D():
            self.vspd = -6*self.Gravity
            self.Tap_Orb = False
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,10])
        #Collision avec Pad Yellow Jump
        if self.Collision_Pad_Yellow_D() == True:
            self.vspd = -8*self.Gravity
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,10])
        #Collision avec Pad Blue Gravity
        if self.Collision_Pad_Blue_D() == True:
            self.vspd = -2*self.Gravity
            if self.Gravity == 1:
                self.Gravity = -1
            else:
                self.Gravity = 1
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,5])

        #Collision au sol
        if self.Collision_Speed_D(): #Si le personnage rentre en collision avec Sol
            self.y = round(self.y) #Arrodir la valeur
            while not self.Collision_y_D(): #Tant qu'il est dans l'écran
                self.y += pyxel.sgn(self.vspd) #Le faire descendre
            if self.Gravity == pyxel.sgn(self.vspd):
                self.isgrounded = True #Il est au sol
            self.vspd = 0 #Il arrête de bouger
            self.rotate = self.rotate%4 #Ne rotationne plus
        else:
            self.isgrounded = False #Il est dans les airs
            if pyxel.frame_count%3 == 0 :
                if self.Gravity == 1:
                    self.rotate += 1 #Rotation en l'air
                else:
                    self.rotate -= 1 #Rotation en l'air inversée

        #Mouvement
        self.y += self.vspd
        if self.Cin_begin == False and self.Cin_fin_Chrono == 100: #Si pas dans la cinématique du début et pas dans cinématique de fin dans portail
            self.x += self.hspd

        #Création Pixel Dust
        if self.isgrounded == True:
            if self.Gravity == 1:
                self.Pixel_Dust_liste.append([self.x,self.y+7,pyxel.rndf(0,1.5)*self.Gravity, 15])
            else:
                self.Pixel_Dust_liste.append([self.x,self.y,pyxel.rndf(0,1.5)*self.Gravity, 15])

        self.hspd = 0

    def Ball_D(self):
        #Avancé vers l'avant
        self.hspd = self.speed

        #Saut
        if (self.Space_p and self.isgrounded == True) or (self.Space and self.Tap_Orb == True and self.isgrounded == True): #Si ESPACE appuyer ou si ESPACE appuyer en l'air
            if self.Gravity == 1:
                self.Gravity = -1
            else:
                self.Gravity = 1

        #Tap une Orb
        if (self.Space_p) and self.isgrounded == False:
            self.Tap_Orb = True
        if self.Tap_Orb == True and not self.Space:
            self.Tap_Orb = False
        if self.isgrounded == True:
            self.Tap_Orb = False

        #Gravité qui change
        if self.Gravity == 1:
            self.vspd = min(6, self.vspd + 0.90) #Argument1 : Vitesse maximale, Argument2 : Accélération
        else:
            self.vspd = max(-6, self.vspd - 0.90) #Argument1 : Vitesse maximale, Argument2 : Accélération

        #Collison avec une Orb
        if self.Tap_Orb == True and self.Collision_Orb_D():
            self.vspd = -6*self.Gravity
            self.Tap_Orb = False
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,10])
        #Collision avec Pad Yellow Jump
        if self.Collision_Pad_Yellow_D() == True:
            self.vspd = -8*self.Gravity
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,10])
        #Collision avec Pad Blue Gravity
        if self.Collision_Pad_Blue_D() == True:
            self.vspd = -2*self.Gravity
            if self.Gravity == 1:
                self.Gravity = -1
            else:
                self.Gravity = 1
            self.Circle_list.append([self.x+self.size/2,self.y+self.size/2,6,5])

        #Collision au sol
        if self.Collision_Speed_D(): #Si le personnage rentre en collision avec Sol
            self.y = round(self.y) #Arrodir la valeur
            while not self.Collision_y_D(): #Tant qu'il est dans l'écran
                self.y += pyxel.sgn(self.vspd) #Le faire descendre
            if self.Gravity == pyxel.sgn(self.vspd):
                self.isgrounded = True #Il est au sol
            self.vspd = 0 #Il arrête de bouger
        else:
            self.isgrounded = False #Il est dans les airs

        if pyxel.frame_count%2 == 0 :
            self.rotate += self.Gravity #Rotation en l'air

        #Mouvement
        self.y += self.vspd
        self.x += self.hspd

        #Création Pixel Dust
        if self.isgrounded == True:
            if self.Gravity == 1:
                self.Pixel_Dust_liste.append([self.x,self.y+7,pyxel.rndf(0,1.5)*self.Gravity, 15])
            else:
                self.Pixel_Dust_liste.append([self.x,self.y,pyxel.rndf(0,1.5)*self.Gravity, 15])

        self.hspd = 0

    def Wave_D(self):
        #Avancé vers l'avant
        self.hspd = self.speed

        #Début Trail
        self.Wave_trail_cords[0][0] = self.x + 4
        self.Wave_trail_cords[0][1] = self.y + self.size/2

        if (self.Space): #Haut/Bas
            self.vspd = -self.speed
            self.rotate = 0
            self.Gravity = -1
        else:
            self.vspd = self.speed
            self.rotate = 1
            self.Gravity = 1

        #Collision au sol
        if self.Collision_Speed_D(): #Si le personnage rentre en collision avec Sol
            self.y = round(self.y) #Arrodir la valeur
            while not self.Collision_y_D(): #Tant qu'il est dans l'écran
                self.y += self.Gravity #Le faire descendre
            self.vspd = 0 #Il arrête de bouger
            self.isgrounded = True #Il est au sol

        else:
            self.isgrounded = False #Il est dans les airs

        #Mouvement
        self.y += self.vspd
        self.x += self.hspd
        #Fin Trail
        self.Wave_trail_cords[1][0] = self.x + 4
        self.Wave_trail_cords[1][1] = self.y + self.size/2

        #Ajout des coordonnées
        self.Wave_Trail_Draw.append((self.Wave_trail_cords[0][0],self.Wave_trail_cords[0][1],self.Wave_trail_cords[1][0],self.Wave_trail_cords[1][1]))

        #Suppression des coordonnées
        for Trail in self.Wave_Trail_Draw:
            if Trail[2] < self.xcam or Trail[0] > self.xcam+128:
                self.Wave_Trail_Draw.remove(Trail)

        self.hspd = 0
        self.Gravity = 1

    def Circle_in_D(self):
        for Circle in self.Circle_list:
            Circle[2] -= 1
            if Circle[2] == 0:
                self.Circle_list.remove(Circle)

    def Circle_out_D(self):
        for Circle in self.Circle_list_out:
            Circle[2] += 1.5
            if Circle[2] > 15:
                self.Circle_list_out.remove(Circle)

    def Death_D(self):
        if self.isdead == False: #Fin du mouvement
            self.isdead = True
            self.Circle_list_out.append([self.x+self.size/2,self.y+self.size/2,8,14])
            pyxel.playm(7)
            pyxel.play(3, 60)

        if self.Death_Chrono == 0: #Réapparition au début du level
            if self.Level_Count == 1:
                self.Start_x = 30
                self.Start_y = 112
            elif self.Level_Count == 2:
                self.Start_x = 158
                self.Start_y = 46*8
            else:
                self.Start_x = 40*8 + 30
                self.Start_y = 78*8
            self.x = self.Start_x
            self.y = self.Start_y
            self.Gravity = 1
            self.Attemps_Count += 1
            self.speed = 2
            self.size = 8
            self.Mode = 0

        if self.Death_Chrono > -10: #Décompte
            self.Death_Chrono -= 1
        else:
            self.Death_Chrono = 30 #Reprise du Mouvement
            self.isdead = False
            if self.Level_Count == 1:
                pyxel.playm(0)
            elif self.Level_Count == 2:
                pyxel.playm(4)
            else:
                pyxel.playm(2)

    def Camera_D(self): #Mouvement Camera
        self.xcam = self.x - 30
        self.ycam = 128*(self.y//128)

    def Background_D(self):
        if len(self.Backgrounds_liste) == 0:
            for kk in range(3):
                self.Backgrounds_liste.append([kk*160])


        for Background in self.Backgrounds_liste:
            Background[0] = Background[0] - 1
            if Background[0] + self.xcam < self.xcam - 200:
                Background[0] = Background[0] + (3*160)

    def Level_D(self):
        if self.x + self.hspd > (128*15) + 30: #Monter d'un niveau
            self.x = 30 + (self.x + self.hspd - (128*15 + 30))
            self.y += 128
        if self.x < 30 and self.y > 128: #Descendre d'un niveau
            self.x = (128*15) + 30 - (30 - self.x)
            self.y -= 128

        if int(self.y)//128 <= 1 or (int(self.y)//128 == 2 and int(self.x) < 158):
            self.Level_Count = 1
        elif (int(self.y)//128 == 2 and int(self.x) >= 158) or (int(self.y)//128 == 3) or (int(self.y)//128 == 4 and int(self.x) < 40*8 + 30):
            self.Level_Count = 2
            if self.Level_Previous == 1:
                pyxel.playm(4)
        else:#int(self.y)//128 == 4 and int(self.x) > 48*8 78*8
            self.Level_Count = 3
            if self.Level_Previous == 2:
                pyxel.playm(2)

        self.Level_Previous = self.Level_Count

    def Cinematic_D(self):
        #Cinématique
        #Début
        if self.Cin_begin == True:
            if self.Cin_Chrono > 0:
                self.y = -680
                self.Cin_Chrono -= 1
            if self.Cin_Chrono <= 0 and self.isgrounded == False:
                    self.Cube_D()
                    if self.infall == False:
                        pyxel.play(3, 15)
                        self.infall = True
            if self.isgrounded == True:
                self.Cin_begin = False

            #Effet bleu sortie du portail
            if (self.Cin_Chrono == 248 or self.Cin_Chrono == 200 or self.Cin_Chrono == 157 or self.Cin_Chrono == 125 or self.Cin_Chrono == 98 or self.Cin_Chrono == 77 or self.Cin_Chrono == 58 or self.Cin_Chrono < 50) and self.Cin_Chrono != 0:
                pyxel.play(3, 14)
                self.Circle_list.append([self.x+self.size/2 - 3,self.y+self.size/2 + 4,5,5])

    def Cinematic_fin_D(self):
        #Cinématique
        #Fin
        if self.Cin_end == 1:
            #entrer dans le portail
            if self.y > 111*8 - 4 and self.x >= 53*8:
                if self.Cin_fin_Chrono > 0:
                    if self.Cin_fin_Chrono == 99:
                        pyxel.play(3, 14)
                        self.Circle_list.append([self.x+self.size/2,self.y+self.size/2 - 12,5,5])
                    self.Cin_fin_Chrono -= 1
                else:
                    self.x = 58*8
                    self.y = 102*8
                    self.Cin_fin_Chrono = 99

        if self.Cin_end == 2:
            if self.Cin_fin_Chrono < 100 and self.Cin_fin_Chrono > 0 and self.x < 68*8:
                if self.Cin_fin_Chrono == 99:
                    pyxel.play(3, 14)
                    self.Circle_list.append([self.x+self.size/2 + 6,self.y+self.size/2 + 2,5,5])
                self.Cin_fin_Chrono -= 1
                if self.Cin_fin_Chrono == 0:
                    self.Cin_fin_Chrono = 100
            if self.x >= 68*8:
                if self.end_of_game == False:
                    pyxel.play(3, 59)
                    self.end_of_game = True
                if self.Cin_fin_Chrono > 0:
                    self.Cin_fin_Chrono -= 1
                if self.Cin_fin_Chrono == 0:
                    La_kk_venture.Jeu = 3
                    La_kk_venture.Initialisation = True
                    pyxel.stop()

    def update(self):
        #Bouton
        self.Space = pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
        self.Space_p = pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

        if self.isdead == False and self.Starting_Screen == False and self.end_of_game == False: #Afficher si vivant
            if self.Mode == 0:
                self.Cube_D()
            if self.Mode == 1:
                self.Ball_D()
            if self.Mode == 2:
                self.Wave_D()
        #Collision
        self.Collision_y_D()
        self.Collision_Speed_D()
        self.Collision_death_D()
        self.Collision_Death_Rampe_D()
        self.Collision_Orb_D()
        self.Circle_in_D()
        self.Circle_out_D()
        self.Collision_Port_Cube_D()
        self.Collision_Port_Ball_D()
        self.Collision_Port_Wave_D()
        self.Collision_Port_Speed_Blue_D()
        self.Collision_Port_Speed_Green_D()
        self.Collision_Port_Speed_Red_D()
        self.Collision_Coin_D()

        #Level
        self.Level_D()
        self.Camera_D()
        self.Background_D()

        #Effet
        self.Pixel_Dust_D()
        self.Tile_Type_Collision = ()
        #Mort si obstacle
        if self.Collision_death_D() or self.Collision_Death_Rampe_D() or self.Death_Chrono < 30:
            self.Death_D()

        #Cinematique début
        self.Cinematic_D()
        self.Cinematic_fin_D()

        #Commencé le jeu
        if self.Starting_Screen == True and self.Cin_begin == False:
            if (self.Space_p) == True:
                self.Starting_Screen = False
                pyxel.playm(0)


        #Test
        if self.y < 0: #Hors Screen en Haut
            self.Gravity = 1
        # if pyxel.btnp(pyxel.KEY_G): #Changement Gravité
        #     if self.Gravity == 1:
        #         self.Gravity = -1
        #     else:
        #         self.Gravity = 1
        # if pyxel.btnp(pyxel.KEY_T): #Téléporter à Fin du Niveau
        #     self.x = 28*8 #(128*14)
        #     self.y = 104*8
        # if pyxel.btnp(pyxel.KEY_D): #Mourir sur place
        #     self.Death_Chrono = 0
        #     self.Death()
        # if pyxel.btnp(pyxel.KEY_P): #Position sur la tilemap
        #     print(self.x//8, self.y//8)
        # if pyxel.btnp(pyxel.KEY_R): #Téléporter à Début du Niveau
        #     self.x = self.Start_x
        #     self.y = self.Start_y
        # if pyxel.btnp(pyxel.KEY_M): #Changer de Mode
        #     if self.Mode == 2:
        #         self.Mode = 0
        #         self.size = 8
        #     else:
        #         self.Mode += 1
        #         if self.Mode == 2:
        #             self.size = 6

    def draw(self):
        if self.Cin_begin == True: #Cinématiquep
            if self.y + 6 < (-710) + 112:
                pyxel.camera(self.x - 30+La_kk_venture.Camera_Buttons, -710)
            else:
                pyxel.camera(self.x - 30+La_kk_venture.Camera_Buttons, self.y - 112)
        else:
            pyxel.camera(self.xcam+La_kk_venture.Camera_Buttons, self.ycam) #Camera mouvement

        #Cinématique fin
        if self.y//128 >= 6 and self.x + self.speed - 30 >= 40*8 and self.x <= 55*8:
            pyxel.camera(40*8+La_kk_venture.Camera_Buttons, 96*8)
            self.Cin_end = 1
            if self.x < 45*8:
                pyxel.playm(7)
        if self.y//128 == 6 and self.x >= 55*8:
            pyxel.camera(56*8+La_kk_venture.Camera_Buttons, 96*8)
            self.Cin_end = 2

        pyxel.cls(0) #Couleur Fond Test
        #Changemennt de couleurs du Background par Niveau
        if self.Level_Count == 1:
            pyxel.pal()
        elif self.Level_Count == 2:
            pyxel.pal(6,11)
            pyxel.pal(12,3)
        elif self.Level_Count == 3:
            pyxel.pal(6,8)
            pyxel.pal(12,2)
        else:
            pyxel.pal()
        if self.Cin_begin == False and self.Cin_end != 2: #Si pas dans la cinématique du début Ni dans la dernière scène
            for Background in self.Backgrounds_liste:
                pyxel.bltm(Background[0] + self.xcam, 128*(self.y//128), 1, 0, 0, 160, 129, 11) #Backgrounds
        pyxel.pal()

        pyxel.bltm(0, 0, 4, 0, 0, 256*8, 128*7, 15) #Level Objects


        for Pixel in self.Pixel_Dust_liste: #Dust
            pyxel.blt(Pixel[0], Pixel[1], 0, 0, 8, 1, 1, 11)

        if self.isdead == False and self.end_of_game == False: #Afficher si vivant
            if self.Mode == 0:
                pyxel.blt(self.x, self.y, 0, 8*(self.rotate%4) + 16, 16, self.size, self.size, 0) #Afficher Joueur Cube
            if self.Mode == 1:
                pyxel.blt(self.x, self.y, 0, 8*(self.rotate%3) + 40, 0, self.size, self.size, 0) #Afficher Joueur Ball
        if self.Mode == 2:
            for Trail in self.Wave_Trail_Draw: #Afficher la trainée
                pyxel.line(Trail[0],Trail[1],Trail[2],Trail[3], 10)
            if self.rotate < 0: #Bug d'affichage quand transformation Ball ==> Wave
                self.rotate = 1
            if self.isdead == False: #Afficher si vivant
                pyxel.blt(self.x, self.y, 0, 8*(self.rotate) + 56, 8, 8, 7, 0) #Afficher Joueur Wave

        if self.Cin_begin == True:
            pyxel.blt(15,-680,0,((pyxel.frame_count//5)%4)*32,88,32,16,15) #Affiche le portail
            for Circle in self.Circle_list: #Cercle qui rétrécit
                pyxel.circ(Circle[0],Circle[1],Circle[2],Circle[3])

        pyxel.blt(52*8,111*8,0,((pyxel.frame_count//5)%4)*32,88,32,16,15) #Affiche les portails de fin
        pyxel.blt(57*8,102*8,0,((pyxel.frame_count//5)%4)*32,88,32,16,15)

        for Circle in self.Circle_list: #Cercle qui rétrécit
            pyxel.circ(Circle[0],Circle[1],Circle[2],Circle[3])
        for Circle in self.Circle_list_out: #Cercle qui s'agrandit
            pyxel.circ(Circle[0],Circle[1],Circle[2],Circle[3])

        pyxel.bltm(0, 0, 3, 0, 0, 256*8, 128*7, 15) #Afficher transitions Level

        if self.Coin_count > 0:
            pyxel.text(self.xcam + (70), self.ycam + 5,"Coins : " + str(self.Coin_count) + "/" + str(self.Coin_max), 10) #Afficher nombre de Coin collectées et à collectées

        #pyxel.text(self.x, self.ycam + 1, str(self.x), 10) #pyxel.tilemap(0).pget(self.x, self.y)
        pyxel.text(self.Start_x +18, self.Start_y - 85, "Attemps " + str(self.Attemps_Count), 10) #Attemps
        pyxel.text(25, 100, "[Espace] pour sauter\nLa NSI c'est la garantie\nde l'emploi dans tous\nles domaines\nMedecine, transport, vente, production ect...", 7) #Tuto Saut


"""
Jeu 3
"""

class Jeu_N:
    def __init__(self):
        pyxel.camera(La_kk_venture.Camera_Buttons,0)
        #initialisation de toutes les variables ainsi que les tableaux
        self.c_deb_nathan = True
        self.attendre_nathan = False

        self.vies_nathan = 20
        self.nbr_vies_nathan = self.vies_nathan // 2
        self.demi_coeur_nathan = self.vies_nathan%2
        self.coeur_vide_nathan = 0
        self.nbr_coeur_vide_nathan = self.coeur_vide_nathan//2

        self.x_tuyau_nathan=0
        self.xcaca_nathan = 0
        self.ycaca_nathan = 112
        self.hspd_nathan = 0
        self.vspd_nathan = 0
        self.size_nathan = 8
        self.sens_nathan = 1
        self.x_sprite_nathan = 0
        self.y_sprite_nathan = 0
        self.isgrounded_nathan = False

        self.liste_plat_un_nathan = [[0, 120, 128, 8]]
        self.liste_plat_deux_nathan=[[14,96,96,8]]
        self.liste_plat_trois_nathan =[[30,72,64,8]]
        self.liste_plat_quatre_nathan=[[47,48,32,8]]
        self.liste_plat_cinq_nathan=[[0,32,24,8],[99,32,24,8]]

        self.tirs_liste_gauche_nathan = []
        self.tirs_liste_droite_nathan = []

        self.ennemis_liste_gauche_monstre_un_nathan=[]
        self.ennemis_liste_droite_monstre_un_nathan=[]

        self.sprite_tentacule_nathan = 51

        self.ennemis_liste_gauche_monstre_deux_nathan=[]
        self.tentacule_gauche_nathan=[]
        self.deplacement_gauche_t_nathan=[]

        self.ennemis_liste_droite_monstre_deux_nathan=[]
        self.tentacule_droite_nathan=[]
        self.deplacement_droite_t_nathan=[]

        self.tir_poulpe_droite_nathan=[]
        self.tir_poulpe_gauche_nathan=[]

        self.x_sprite_monstre_un_nathan = 0
        self.x_sprite_monstre_deux_nathan=0

        self.explosions_liste_nathan=[]
        self.sang_un_nathan=[]
        self.sang_deux_nathan=[]

        self.background_liste_nathan=[[0,0],[127.5,0],[255.5,0]]

        self.avant_bazooka_nathan = False
        self.bazooka_nathan = False
        self.boss_nathan = False
        self.en_train_de_tirer_nathan = False

        self.ennemis_killed_nathan = 0

        self.Chronodukk = 0
        self.temps_un_nathan= 400
        self.temps_deux_nathan=1000
        self.explosion_chrono_nathan=60
        self.chrono_boss_nathan = 50
        self.vasy_mon_rey_nathan = False

        self.kk_dead_nathan= False

        self.the_B_nathan= []
        self.combat_final_nathan = False
        self.laser_nathan = False
        self.touche_par_le_boss_nathan = False
        self.couldown_nathan = False
        self.chrono_couldown_nathan =0

        self.vaisseau_sen_va_nathan = False
        self.liste_coordonees_vaisseau_nathan=[]


        pyxel.load('kkventure_nathan.pyxres')

        pyxel.playm(1,0,True)

    def c_debut_nathan(self) :# Cette fonction me sert a lancer la cinématique de début pour lancer mon jeu.
        if self.xcaca_nathan == 8 :
            pyxel.play(0,58)
        if self.xcaca_nathan == 18 :
            self.attendre_nathan = True
            self.xcaca_nathan+=0.5
        if self.Chronodukk%60 == 59 :
            self.attendre_nathan = False
        if self.attendre_nathan == False:
            self.xcaca_nathan+=0.5
        if self.xcaca_nathan >= 54 :
            self.c_deb_nathan=False

    def tuyau_nathan(self) : #Fais disparaitre le tuyau avec le défilement automatique
        self.x_tuyau_nathan-=0.5


    def joueur_nathan (self) : #Cette fonction va s'occupper de tout les déplacements du personnages : vers le haut, vers le bas, la gauche et la droite.

        if La_kk_venture.Down_p :
            if self.ycaca_nathan<111 and self.isgrounded_nathan== True :

                self.ycaca_nathan+=5
                self.isgrounded_nathan = False

        if La_kk_venture.Right and self.xcaca_nathan < 120:
            self.xcaca_nathan += 2
            self.sens_nathan = 1
            if pyxel.frame_count%6 < 3 :
                self.y_sprite_nathan = 8
                self.x_sprite_nathan = 0
            else :
                self.y_sprite_nathan = 8
                self.x_sprite_nathan = 8
        else :
            self.y_sprite_nathan = 0
            self.x_sprite_nathan = 0

        if La_kk_venture.Left and self.xcaca_nathan > 0:
            self.xcaca_nathan += -2
            self.sens_nathan = -1
            if pyxel.frame_count%6 < 3 :
                self.y_sprite_nathan = 8
                self.x_sprite_nathan = 0
            else :
                self.y_sprite_nathan = 8
                self.x_sprite_nathan = 8


        if La_kk_venture.Up_p and self.isgrounded_nathan == True :
            self.vspd_nathan =-7

        self.vspd_nathan =min(6,self.vspd_nathan + 0.90)

        if self.ycaca_nathan + self.vspd_nathan > pyxel.height- self.size_nathan :
            self.ycaca_nathan = round(self.ycaca_nathan)
            while not self.ycaca_nathan + 1> pyxel.height-self.size_nathan :
                self.ycaca_nathan += 1
            self.vspd_nathan =0
            self.isgrounded_nathan =True


        else :
            self.isgrounded_nathan = False

        self.ycaca_nathan += self.vspd_nathan
        self.xcaca_nathan += self.hspd_nathan




    def sur_plat_un_nathan(self): #Cette fonction va tester toutes les colisions avec toutes les plateformes dans les tableaux de plateformes. cest la meme fonction plusieurs fois pour plusieurs plateformes. Je suis obligé de faire dans différents tableaux car ensuite je dois les déplacer et cest trop (TROP) compliqué en un seul tableau.
        for plat in self.liste_plat_un_nathan:
            if self.ycaca_nathan +8 > plat[1]:
                if self.ycaca_nathan+8  <= plat[1]+plat[3] and self.xcaca_nathan > plat[0]-8 and self.xcaca_nathan < plat[0]+plat[2] :
                    self.ycaca_nathan = plat[1] -8
                    self.isgrounded_nathan = True
                    return True
        self.isgrounded_nathan = False
        for plat in self.liste_plat_deux_nathan:
            if self.ycaca_nathan +8 > plat[1]:
                if self.ycaca_nathan+8  <= plat[1]+plat[3] and self.xcaca_nathan > plat[0]-8 and self.xcaca_nathan < plat[0]+plat[2] :
                    self.ycaca_nathan = plat[1] -8
                    self.isgrounded_nathan = True
                    return True
        self.isgrounded_nathan = False
        for plat in self.liste_plat_trois_nathan:
            if self.ycaca_nathan +8 > plat[1]:
                if self.ycaca_nathan+8  <= plat[1]+plat[3] and self.xcaca_nathan > plat[0]-8 and self.xcaca_nathan < plat[0]+plat[2] :
                    self.ycaca_nathan = plat[1] -8
                    self.isgrounded_nathan = True
                    return True
        self.isgrounded_nathan = False
        for plat in self.liste_plat_quatre_nathan:
            if self.ycaca_nathan +8 > plat[1]:
                if self.ycaca_nathan+8  <= plat[1]+plat[3] and self.xcaca_nathan > plat[0]-8 and self.xcaca_nathan < plat[0]+plat[2] :
                    self.ycaca_nathan = plat[1] -8
                    self.isgrounded_nathan = True
                    return True
        self.isgrounded_nathan = False
        for plat in self.liste_plat_cinq_nathan:
            if self.ycaca_nathan +8 > plat[1]:
                if self.ycaca_nathan+8  <= plat[1]+plat[3] and self.xcaca_nathan > plat[0]-8 and self.xcaca_nathan < plat[0]+plat[2] :
                    self.ycaca_nathan = plat[1] -8
                    self.isgrounded_nathan = True
                    return True
        self.isgrounded_nathan = False







    def tirs_droite_nathan(self) : #Cette fonction(divisé en deux) sert a tirer ou a utiliser la capacité spéciale quand le personnage est tourné vers la droite.
        if self.bazooka_nathan == False and self.en_train_de_tirer_nathan == False:
            if La_kk_venture.Space_p and self.sens_nathan == 1:
                self.tirs_liste_droite_nathan.append([self.xcaca_nathan+12, self.ycaca_nathan+3])
                pyxel.play(0, 63)


            for tir in self.tirs_liste_droite_nathan:
                    tir[0] += 5
                    if  tir[0]>=128:
                        self.tirs_liste_droite_nathan.remove(tir)
        else :
            self.tirs_liste_droite_nathan = []
            self.tirs_liste_gauche_nathan = []
            if La_kk_venture.Space_p and self.sens_nathan == 1 and self.bazooka_nathan == True:
                for kk in range (100) :
                    if kk%2 == 0 :
                        self.explosions_liste_nathan.append([self.xcaca_nathan+11,self.ycaca_nathan+2,kk])
                self.boss_nathan = True
                self.bazooka_nathan= False
                self.en_train_de_tirer_nathan = True
                pyxel.play(0,61)
                self.vies_nathan = 20
                self.coeur_vide_nathan=0



    def tirs_gauche_nathan(self) :# Idem mais vers la gauche
        if self.bazooka_nathan == False and self.en_train_de_tirer_nathan == False :
            if La_kk_venture.Space_p and self.sens_nathan == -1:
                self.tirs_liste_gauche_nathan.append([self.xcaca_nathan+-3, self.ycaca_nathan+3])
                pyxel.play(0, 63)


            for tir in self.tirs_liste_gauche_nathan:
                    tir[0] -= 5
                    if  tir[0]<-8:
                        self.tirs_liste_gauche_nathan.remove(tir)
        else :
            self.tirs_liste_droite_nathan = []
            self.tirs_liste_gauche_nathan = []
            if La_kk_venture.Space_p and self.sens_nathan == -1 and self.bazooka_nathan == True:
                for kk in range (100) :
                    if kk%2 == 0 :
                        self.explosions_liste_nathan.append([self.xcaca_nathan-10,self.ycaca_nathan,kk])
                self.boss_nathan = True
                self.bazooka_nathan = False
                self.en_train_de_tirer_nathan = True
                pyxel.play(0,61)
                self.vies_nathan = 20
                self.coeur_vide_nathan=0






    def ennemis_creation_gauche_monstre_un_nathan(self): #cette fonction fais apparaitre les petites monstres a gauche.
        if (self.Chronodukk % self.temps_un_nathan==0):
            self.ennemis_liste_gauche_monstre_un_nathan.append([0, random.randint(20, 112)])

    def ennemis_deplacement_gauche_monstre_un_nathan(self): #Cette fonction les fais se déplacer.
        for ennemi in self.ennemis_liste_gauche_monstre_un_nathan:
            ennemi[0] += 1
            if  ennemi[0]>128:
                self.ennemis_liste_gauche_monstre_un_nathan.append([-8, ennemi[1]])
                self.ennemis_liste_gauche_monstre_un_nathan.remove(ennemi)


    def ennemis_suppression_a_gauche_monstre_gauche_un_nathan(self): #Cette fonction fais les colisions entre les tirs a gauche et les monstres venant de gauche et fais une petite explosion avec du sang si lennemi est touché

        for monstre in self.ennemis_liste_gauche_monstre_un_nathan:
            for i in self.tirs_liste_gauche_nathan:
                if i[0]<=monstre[0]+7 and i[0]>=monstre[0] :
                    if i[1]>monstre[1]-7 and i[1]<monstre[1]+7 :
                        self.tirs_liste_gauche_nathan.remove(i)
                        self.ennemis_liste_gauche_monstre_un_nathan.remove(monstre)
                        self.explosions_liste_nathan.append([i[0],i[1],0])
                        self.explosions_liste_nathan.append([i[0],i[1],2])
                        self.sang_un_nathan.append([monstre[0],monstre[1],0,88])
                        pyxel.play(0, 62)
                        self.ennemis_killed_nathan +=1

    def ennemis_suppression_a_droite_monstre_gauche_un_nathan(self):#Cette fonction fais les colisions entre les tirs a droite et les monstres venant de gauche et fais une petite explosion avec du sang si lennemi est touché

        for monstree in self.ennemis_liste_gauche_monstre_un_nathan:
            for k in self.tirs_liste_droite_nathan:
                if k[0]>monstree[0]-7 and k[0]<monstree[0] :
                    if k[1]>monstree[1]-7 and k[1]<monstree[1]+7 :
                        self.tirs_liste_droite_nathan.remove(k)
                        self.ennemis_liste_gauche_monstre_un_nathan.remove(monstree)
                        self.explosions_liste_nathan.append([k[0],k[1],0])
                        self.explosions_liste_nathan.append([k[0],k[1],2])
                        self.sang_un_nathan.append([monstree[0],monstree[1],0,88])
                        pyxel.play(0, 62)
                        self.ennemis_killed_nathan +=1



    def ennemis_creation_droite_monstre_un_nathan(self):#cette fonction fais apparaitre les petites monstres a droite.
        if (self.Chronodukk % self.temps_un_nathan==0):
            self.ennemis_liste_droite_monstre_un_nathan.append([128, random.randint(20, 112)])

    def ennemis_deplacement_droite_monstre_un_nathan(self): #Cette fonction les fais se déplacer
        for ennemi in self.ennemis_liste_droite_monstre_un_nathan:
            ennemi[0] -= 1
            if  ennemi[0]<-8:
                self.ennemis_liste_droite_monstre_un_nathan.append([128, ennemi[1]])
                self.ennemis_liste_droite_monstre_un_nathan.remove(ennemi)


    def ennemis_suppression_a_gauche_monstre_droite_un_nathan(self):#Cette fonction fais les colisions entre les tirs a gauche et les monstres venant de droite et fais une petite explosion avec du sang si lennemi est touché


        for ouiiii in self.ennemis_liste_droite_monstre_un_nathan:
            for nonnnn in self.tirs_liste_gauche_nathan:
                if nonnnn[0]<ouiiii[0]+7 and nonnnn[0]>ouiiii[0] :
                    if nonnnn[1]>ouiiii[1]-7 and nonnnn[1]<ouiiii[1]+7 :
                        self.tirs_liste_gauche_nathan.remove(nonnnn)
                        self.ennemis_liste_droite_monstre_un_nathan.remove(ouiiii)
                        self.explosions_liste_nathan.append([nonnnn[0],nonnnn[1],0])
                        self.explosions_liste_nathan.append([nonnnn[0],nonnnn[1],2])
                        self.sang_un_nathan.append([ouiiii[0],ouiiii[1],0,88])
                        pyxel.play(0, 62)
                        self.ennemis_killed_nathan +=1


    def ennemis_suppression_a_droite_monstre_droite_un_nathan(self):
        #Cette fonction fais les colisions entre les tirs a droite et les monstres venant de droite et fais une petite explosion avec du sang si lennemi est touché

        for tacos in self.ennemis_liste_droite_monstre_un_nathan:
            for grec in self.tirs_liste_droite_nathan:
                if grec[0]>tacos[0]-7 and grec[0]<tacos[0] :
                    if grec[1]>tacos[1]-7 and grec[1]<tacos[1]+7 :
                        self.tirs_liste_droite_nathan.remove(grec)
                        self.ennemis_liste_droite_monstre_un_nathan.remove(tacos)
                        self.explosions_liste_nathan.append([grec[0],grec[1],0])
                        self.explosions_liste_nathan.append([grec[0],grec[1],2])
                        self.sang_un_nathan.append([tacos[0],tacos[1],0,88])
                        pyxel.play(0, 62)
                        self.ennemis_killed_nathan +=1











    def ennemis_creation_gauche_monstre_deux_nathan(self) :#cette fonction fais apparaitre les gros monstres a gauche
        if (self.Chronodukk % self.temps_deux_nathan==0) :
            self.ennemis_liste_gauche_monstre_deux_nathan.append([-16, self.ycaca_nathan-5, 10])

    def ennemis_deplacement_gauche_monstre_deux_nathan(self): # leur déplacement
        for ennemi in self.ennemis_liste_gauche_monstre_deux_nathan:
            if ennemi[0]<6 :
                ennemi[0] += 0.2
            if self.ycaca_nathan>ennemi[1] :
                ennemi[1]+=0.3
            else :
                ennemi[1]-=0.3
    def ennemis_suppression_monstre_gauche_deux_nathan(self): # les colisions et les explosions

        for ennemi in self.ennemis_liste_gauche_monstre_deux_nathan:
            for tir in self.tirs_liste_gauche_nathan:
                if tir[0]<=ennemi[0]+7 and tir[0]>=ennemi[0] :
                    if tir[1]>ennemi[1]-7 and tir[1]<ennemi[1]+14 :
                        self.tirs_liste_gauche_nathan.remove(tir)
                        self.explosions_liste_nathan.append([tir[0],tir[1],0])
                        self.explosions_liste_nathan.append([tir[0],tir[1],2])
                        ennemi[2]-=1
                        pyxel.play(0, 62)
                        if ennemi[2] < 1 :
                            self.ennemis_liste_gauche_monstre_deux_nathan.remove(ennemi)
                            self.sang_deux_nathan.append([ennemi[0],ennemi[1],0,])
                            self.tentacule_gauche_nathan.append([ennemi[0]+12,ennemi[1]-8])
                            self.tentacule_gauche_nathan.append([ennemi[0]-6,ennemi[1]])
                            self.tentacule_gauche_nathan.append([ennemi[0]+10,ennemi[1]+10])
                            self.ennemis_killed_nathan +=2


    def ennemis_creation_droite_monstre_deux_nathan(self):#cette fonction fais apparaitre les gros monstres a droite
        if (self.Chronodukk % self.temps_deux_nathan==0):
            self.ennemis_liste_droite_monstre_deux_nathan.append([128, self.ycaca_nathan-5, 10])

    def ennemis_deplacement_droite_monstre_deux_nathan(self): #leur déplacement
        for ennemi in self.ennemis_liste_droite_monstre_deux_nathan:
            if ennemi[0]>106 :
                ennemi[0] -= 0.2
            if self.ycaca_nathan>ennemi[1] :
                ennemi[1]+=0.3
            else :
                ennemi[1]-=0.3

    def ennemis_suppression_monstre_droite_deux_nathan(self): # les explosions et les colisions

        for ennemi in self.ennemis_liste_droite_monstre_deux_nathan:
            for tir in self.tirs_liste_droite_nathan:
                if tir[0]>ennemi[0]-7 and tir[0]<ennemi[0] :
                    if tir[1]>ennemi[1]-7 and tir[1]<ennemi[1]+14 :
                        self.tirs_liste_droite_nathan.remove(tir)
                        self.explosions_liste_nathan.append([tir[0]+8,tir[1],0])
                        self.explosions_liste_nathan.append([tir[0]+8,tir[1],2])
                        ennemi[2]-=1
                        pyxel.play(0, 62)
                        if ennemi[2] < 1 :
                            self.ennemis_liste_droite_monstre_deux_nathan.remove(ennemi)
                            self.sang_deux_nathan.append([ennemi[0],ennemi[1],0,])
                            self.tentacule_droite_nathan.append([ennemi[0]+12,ennemi[1]-8])
                            self.tentacule_droite_nathan.append([ennemi[0]-6,ennemi[1]])
                            self.tentacule_droite_nathan.append([ennemi[0]+10,ennemi[1]+10])
                            self.ennemis_killed_nathan +=2


    def apparition_tir_poulpe_droite_nathan(self) : # le tir du gros monstre(oui il tire) a droite
        for kk in self.ennemis_liste_droite_monstre_deux_nathan :
            if pyxel.frame_count%60 == 59 :
                self.tir_poulpe_droite_nathan.append([kk[0],kk[1]+5])

    def deplacement_tir_poulpe_droite_nathan(self) :# son déplacement
        for kk in self.tir_poulpe_droite_nathan :
            kk[0]-=3
            if kk[0]<0 :
                self.tir_poulpe_droite_nathan.remove(kk)

    def apparition_tir_poulpe_gauche_nathan(self) :# idem a gauche
        for kk in self.ennemis_liste_gauche_monstre_deux_nathan :
            if pyxel.frame_count%65 == 48 :
                self.tir_poulpe_gauche_nathan.append([kk[0]+16,kk[1]+5])

    def deplacement_tir_poulpe_gauche_nathan(self) :# idem (deplacement)
        for kk in self.tir_poulpe_gauche_nathan :
            kk[0]+=3
            if kk[0]>128 :
                self.tir_poulpe_gauche_nathan.remove(kk)







    def tentacule_a_gauche_nathan(self) : # Quand le gros monstre meurt il fais apparaitre 3 tentacules qui vont foncer chacunbe a leur tour vers mon personnage, je fais leurs apparition et leurs deplacement avec ces 4 fonctions
        if len(self.tentacule_gauche_nathan)>0 :
            if pyxel.frame_count%50 == 49 :
                self.deplacement_gauche_t_nathan.append(self.tentacule_gauche_nathan[0])
                self.tentacule_gauche_nathan.pop(0)

    def tentacule_a_droite_nathan(self) :
        if len(self.tentacule_droite_nathan)>0 :
            if pyxel.frame_count%50 == 49 :
                self.deplacement_droite_t_nathan.append(self.tentacule_droite_nathan[0])
                self.tentacule_droite_nathan.pop(0)

    def deplacement_des_tentacules_gauches_nathan(self) :
        for ennemi in self.deplacement_gauche_t_nathan :
            if ennemi[0]<128 :
                ennemi[0]+=3
            else :
                self.deplacement_gauche_t_nathan.remove(ennemi)

    def deplacement_des_tentacules_droites_nathan(self) :
        for ennemi in self.deplacement_droite_t_nathan :
            if ennemi[0] > 0 :
                ennemi[0]-=3
            else :
                self.deplacement_droite_t_nathan.remove(ennemi)









    def explosions_animation_nathan(self): #Cette fonction s'occupe de la mini explosion lorsque je tire sur un ennemi ou lorsque je suis touché
        if self.en_train_de_tirer_nathan == False  :
            for explosion in self.explosions_liste_nathan:
                explosion[2] +=1
                if explosion[2] == 12:
                    self.explosions_liste_nathan.remove(explosion)
        elif self.en_train_de_tirer_nathan == True :
            for explosion in self.explosions_liste_nathan:
                explosion[2] +=5
                if explosion[2] == 130:
                    self.explosions_liste_nathan.remove(explosion)


    def sang_de_la_veine_un_nathan(self) : # pareil que l'explosion mais la cest du sang
        for sang in self.sang_un_nathan :
            if pyxel.frame_count%2 == 1 :
                sang[2]+=8
            if sang[2]>50 :
                self.sang_un_nathan.remove(sang)

    def sang_de_la_veine_deux_nathan(self) :# pareil que l'explosion mais la cest du sang (cette fois pour le gros monstre)
        for sang in self.sang_deux_nathan :
            if pyxel.frame_count%3 == 1 :
                sang[2]+=16
            if sang[2]>104 :
                self.sang_deux_nathan.remove(sang)






    def background_nathan(self) : # Cette fonction va s'occuper de déplacer les images en fond pour creer un défilement automatique. Le principe est de mettre trois backgrouns, quand un arrive trop a gauche il est remis a droite pour revenir et ainsi que ce soit infini.
        for jsp in self.background_liste_nathan :
            jsp[0] = jsp[0]-0.5
            if jsp[0] < -128 :
                jsp[0]=self.background_liste_nathan[2][0]+128
                self.background_liste_nathan.append(jsp)
                self.background_liste_nathan.pop(0)


    def deplacement_plateformes_deux_nathan(self) : # Cette longue série de plusieurs fonctions(qui sont les memes) vont s'occuper de gerer le deplacement des plateformes en meme temps que les images pour ainsi creer des plateformes qui se deplacent. Je suis obligé de faire un deplacement spécifique pour chaque plateformes en raison de leur difference de taille ce qui explique que jutilise plusieurs tableaux et donc, plusieurs fonstions.
        if len(self.liste_plat_deux_nathan) == 1 :
            if self.liste_plat_deux_nathan[0][0]>0 :
                self.liste_plat_deux_nathan[0][0]-=0.5
            else :
                self.liste_plat_deux_nathan.append([127,96,0,8])
        elif len(self.liste_plat_deux_nathan) == 2 :
            if self.liste_plat_deux_nathan[0][2] > 0 :
                self.liste_plat_deux_nathan[0][2]-=0.5
                self.liste_plat_deux_nathan[1][0]-=0.5
                self.liste_plat_deux_nathan[1][2]+=0.5
            else :
                self.liste_plat_deux_nathan.pop(0)

    def deplacement_plateformes_trois_nathan(self) :
        if len(self.liste_plat_trois_nathan) == 1 :
            if self.liste_plat_trois_nathan[0][0]>0 :
                self.liste_plat_trois_nathan[0][0]-=0.5
            else :
                self.liste_plat_trois_nathan.append([127,72,0,8])
        elif len(self.liste_plat_trois_nathan) == 2 :
            if self.liste_plat_trois_nathan[0][2] > 0 :
                self.liste_plat_trois_nathan[0][2]-=0.5
                self.liste_plat_trois_nathan[1][0]-=0.5
                self.liste_plat_trois_nathan[1][2]+=0.5
            else :
                self.liste_plat_trois_nathan.pop(0)

    def deplacement_plateformes_quatre_nathan(self) :
        if len(self.liste_plat_quatre_nathan) == 1 :
            if self.liste_plat_quatre_nathan[0][0]>0 :
                self.liste_plat_quatre_nathan[0][0]-=0.5
            else :
                self.liste_plat_quatre_nathan.append([127,48,0,8])
        elif len(self.liste_plat_quatre_nathan) == 2 :
            if self.liste_plat_quatre_nathan[0][2] > 0 :
                self.liste_plat_quatre_nathan[0][2]-=0.5
                self.liste_plat_quatre_nathan[1][0]-=0.5
                self.liste_plat_quatre_nathan[1][2]+=0.5
            else :
                self.liste_plat_quatre_nathan.pop(0)

    def deplacement_plateformes_cinq_nathan(self) :
        if len(self.liste_plat_cinq_nathan) == 1 :
            if self.liste_plat_cinq_nathan[0][0]>0 :
                self.liste_plat_cinq_nathan[0][0]-=0.5
            else :
                self.liste_plat_cinq_nathan.append([127,32,0,8])
        elif len(self.liste_plat_cinq_nathan) == 2 :
            if self.liste_plat_cinq_nathan[0][2] > 0 :
                self.liste_plat_cinq_nathan[0][2]-=0.5
                self.liste_plat_cinq_nathan[1][0]-=0.5
                self.liste_plat_cinq_nathan[1][2]+=0.5
            else :
                self.liste_plat_cinq_nathan.pop(0)




    def deplacement_avec_la_plateforme_nathan(self) :# Si le personnage ne bouge pas, il se deplace en meme temps que la plateforme.
        if self.isgrounded_nathan == True and self.xcaca_nathan>0 :
            self.xcaca_nathan -= 0.5


    def kk_touche_monstre_un_gauche_nathan(self) : # Cette série de "if"(plusieurs fois les memes) sert a tester toutes les colisions du personnage avec tout les monstres pour perdre une vie.
        for ennemi in self.ennemis_liste_gauche_monstre_un_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.ennemis_liste_gauche_monstre_un_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)

    def kk_touche_monstre_un_droite_nathan(self) :
        for ennemi in self.ennemis_liste_droite_monstre_un_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.ennemis_liste_droite_monstre_un_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)

    def kk_touche_poulpe_droite_nathan(self) :
        for ennemi in self.tir_poulpe_droite_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.tir_poulpe_droite_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)

    def kk_touche_poulpe_gauche_nathan(self) :
        for ennemi in self.tir_poulpe_gauche_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.tir_poulpe_gauche_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)

    def kk_touche_tentacule_gauche_nathan(self) :
        for ennemi in self.deplacement_gauche_t_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.deplacement_gauche_t_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)

    def kk_touche_tentacule_droite_nathan(self) :
        for ennemi in self.deplacement_droite_t_nathan :
            if ennemi[0] > self.xcaca_nathan -7 and ennemi[0] and ennemi[0]<self.xcaca_nathan+7 and ennemi[1]>self.ycaca_nathan-7 and ennemi[1]<self.ycaca_nathan +7 :
                        self.deplacement_droite_t_nathan.remove(ennemi)
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],0])
                        self.explosions_liste_nathan.append([ennemi[0],ennemi[1],2])
                        self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
                        self.vies_nathan-=1
                        self.coeur_vide_nathan+=1
                        pyxel.play(0, 62)





    def initialisation_nathan(self) : #Cette fonction initialisation va permettre de gerer certains temps comme le temps dapparitions des monstres ou par exemple le couldown du laser contre le boss. Elle va aussi gerer la capacité spéciale du bazooka qui ne sera utilisable que au bout de 50 ennemis tués.
        if self.ennemis_killed_nathan > 49 and self.bazooka_nathan == False and self.boss_nathan == False:
            self.avant_bazooka_nathan = True
        if self.avant_bazooka_nathan == True :
            La_kk_venture.Press_F = True #Afficher touche F
            if La_kk_venture.F_p :
                self.avant_bazooka_nathan = False
                self.bazooka_nathan = True




        if self.Chronodukk%(15*30)==0 :
            if self.temps_un_nathan>60:
                self.temps_un_nathan -=30
        if self.Chronodukk%(15*30)==0 :
            if self.temps_deux_nathan>100 :
                self.temps_deux_nathan-=30
        if self.en_train_de_tirer_nathan == True :
            self.explosion_chrono_nathan-=1
        if self.explosion_chrono_nathan == 0 :
            self.en_train_de_tirer_nathan = False
        if self.boss_nathan == True :
            self.chrono_boss_nathan -=1
        if  self.chrono_boss_nathan == 0 :
            self.vasy_mon_rey_nathan = True

        if pyxel.frame_count%1 == 0 and self.couldown_nathan == True:
            self.chrono_couldown_nathan+=1

        if self.couldown_nathan == True :
            if self.chrono_couldown_nathan%30 == 0 :
                self.couldown_nathan = False
                self.touche_par_le_boss_nathan = False


        if self.touche_par_le_boss_nathan == True :
            if self.couldown_nathan == False :
                self.vies_nathan-=5
                self.coeur_vide_nathan+=5
            self.couldown_nathan = True




    def enfin_le_boss_nathan(self) : # Cette fonction va dans un premier temps faire disparaitre tous les monstres pour laisser la place au boss. Elle va ensuite gerer le combat final contre le boss et ainsi lancer la cinémlatique de fin de mon jeu.

        if self.vasy_mon_rey_nathan == True :
            for monstre in self.ennemis_liste_gauche_monstre_un_nathan:
                self.sang_un_nathan.append([monstre[0],monstre[1],0,88])
            for monstre in self.ennemis_liste_droite_monstre_un_nathan:
                self.sang_un_nathan.append([monstre[0],monstre[1],0,88])
            for ennemi in self.ennemis_liste_gauche_monstre_deux_nathan:
                self.sang_deux_nathan.append([ennemi[0],ennemi[1],0])
            for ennemi in self.ennemis_liste_droite_monstre_deux_nathan:
                self.sang_deux_nathan.append([ennemi[0],ennemi[1],0])
            for ennemi in self.deplacement_gauche_t_nathan :
                self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
            for ennemi in self.deplacement_droite_t_nathan :
                self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
            for ennemi in self.tir_poulpe_gauche_nathan :
                self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])
            for ennemi in self.tir_poulpe_droite_nathan :
                self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88+8])

            self.ennemis_liste_gauche_monstre_un_nathan=[]
            self.ennemis_liste_droite_monstre_un_nathan=[]

            self.sprite_tentacule_nathan = 51

            self.ennemis_liste_gauche_monstre_deux_nathan=[]
            self.tentacule_gauche_nathan=[]
            self.deplacement_gauche_t_nathan=[]

            self.ennemis_liste_droite_monstre_deux_nathan=[]
            self.tentacule_droite_nathan=[]
            self.deplacement_droite_t_nathan=[]

            self.tir_poulpe_droite_nathan=[]
            self.tir_poulpe_gauche_nathan=[]

            if self.laser_nathan == True :
                if self.ycaca_nathan > self.the_B_nathan[0][1] and self.ycaca_nathan < self.the_B_nathan[0][1]+12 :
                    self.touche_par_le_boss_nathan= True




            if len(self.the_B_nathan) == 0 :
                self.the_B_nathan.append([160,64,50])
            for bosss in self.the_B_nathan :
                if bosss [0]>109 :
                    bosss[0]-=0.5
                if bosss[0] == 109 :
                    self.combat_final_nathan = True
                if bosss[1]<self.ycaca_nathan-6 and self.laser_nathan == False :
                    bosss[1]+=1
                elif bosss[1]>self.ycaca_nathan-6 and self.laser_nathan== False:
                    bosss[1]-=1
            if self.combat_final_nathan == True :
                if self.Chronodukk%210>150 :
                    self.laser_nathan = True
                else :
                    self.laser_nathan = False
            for tir in self.tirs_liste_droite_nathan :
                for ennemi in self.the_B_nathan :
                    if tir[0]>ennemi[0]-7 and tir[0]<ennemi[0] :
                        if tir[1]>ennemi[1]-7 and tir[1]<ennemi[1]+14 :
                            ennemi[2]-=1
                            self.tirs_liste_droite_nathan.remove(tir)
                            self.explosions_liste_nathan.append([ennemi[0]-5,ennemi[1]+3,0])
                            self.explosions_liste_nathan.append([ennemi[0]-5,ennemi[1]+3,2])
                            if ennemi[2] == 0 :
                                self.liste_coordonees_vaisseau_nathan.append([ennemi[0]+4,ennemi[1]+4])
                                self.sang_deux_nathan.append([ennemi[0],ennemi[1],0])
                                self.sang_un_nathan.append([ennemi[0],ennemi[1],0,88])
                                self.sang_un_nathan.append([ennemi[0]+8,ennemi[1],0,88])
                                self.sang_un_nathan.append([ennemi[0],ennemi[1]+8,0,88])
                                self.sang_un_nathan.append([ennemi[0]+8,ennemi[1]+8,0,88])
                                self.vasy_mon_rey_nathan = False
                                self.combat_final_nathan = False
                                self.the_B_nathan.remove(ennemi)
                                pyxel.play(0,59)



    def vaisseau_se_deplace_nathan(self) : # Ces deux dernieres fonctions vont gerer la cinematique de fin qui sera la transition vers le jeu de Adam.
        for v in self.liste_coordonees_vaisseau_nathan :
            if v[1]!= 112 :
                v[1]+=1
            elif v[0] > self.xcaca_nathan -7 and v[0] and v[0]<self.xcaca_nathan+7 and v[1]>self.ycaca_nathan-7 and v[1]<self.ycaca_nathan +7 :
                self.vaisseau_sen_va_nathan = True
                self.xcaca_nathan = 256
                self.ycaca_nathan= 256

    def cinematique_de_fin_nathan(self) : #tout est dans le nom...
        for v in self.liste_coordonees_vaisseau_nathan :
            v[1]-=2
            if v[1] < -16 :
                self.le_jeu_est_fini_nathan = True
                La_kk_venture.Jeu = 4
                La_kk_venture.Initialisation = True
                pyxel.stop()



    def update(self):
        self.Chronodukk += 1

        if self.c_deb_nathan == True and self.kk_dead_nathan==False :
            self.c_debut_nathan()
            self.sur_plat_un_nathan()
        elif self.kk_dead_nathan == False and self.boss_nathan == False :
            self.tuyau_nathan()
            self.joueur_nathan()
            self.sur_plat_un_nathan()

            self.tirs_droite_nathan()
            self.tirs_gauche_nathan()

            self.ennemis_creation_gauche_monstre_un_nathan()
            self.ennemis_deplacement_gauche_monstre_un_nathan()
            self.ennemis_suppression_a_gauche_monstre_gauche_un_nathan()
            self.ennemis_suppression_a_droite_monstre_gauche_un_nathan()

            self.ennemis_creation_droite_monstre_un_nathan()
            self.ennemis_deplacement_droite_monstre_un_nathan()
            self.ennemis_suppression_a_gauche_monstre_droite_un_nathan()
            self.ennemis_suppression_a_droite_monstre_droite_un_nathan()


            self.ennemis_creation_gauche_monstre_deux_nathan()
            self.ennemis_deplacement_gauche_monstre_deux_nathan()
            self.ennemis_suppression_monstre_gauche_deux_nathan()

            self.ennemis_creation_droite_monstre_deux_nathan()
            self.ennemis_deplacement_droite_monstre_deux_nathan()
            self.ennemis_suppression_monstre_droite_deux_nathan()

            self.apparition_tir_poulpe_gauche_nathan()
            self.deplacement_tir_poulpe_gauche_nathan()
            self.apparition_tir_poulpe_droite_nathan()
            self.deplacement_tir_poulpe_droite_nathan()

            self.tentacule_a_gauche_nathan()
            self.tentacule_a_droite_nathan()
            self.deplacement_des_tentacules_gauches_nathan()
            self.deplacement_des_tentacules_droites_nathan()

            self.explosions_animation_nathan()
            self.sang_de_la_veine_un_nathan()
            self.sang_de_la_veine_deux_nathan()

            self.background_nathan()

            self.deplacement_plateformes_deux_nathan()
            self.deplacement_plateformes_trois_nathan()
            self.deplacement_plateformes_quatre_nathan()
            self.deplacement_plateformes_cinq_nathan()
            self.deplacement_avec_la_plateforme_nathan()



            self.kk_touche_monstre_un_droite_nathan()
            self.kk_touche_monstre_un_gauche_nathan()
            self.kk_touche_poulpe_droite_nathan()
            self.kk_touche_poulpe_gauche_nathan()
            self.kk_touche_tentacule_droite_nathan()
            self.kk_touche_tentacule_gauche_nathan()



            self.initialisation_nathan()
            self.enfin_le_boss_nathan()

        elif self.boss_nathan == True and self.vaisseau_sen_va_nathan == False :

            self.joueur_nathan()
            self.sur_plat_un_nathan()

            self.tirs_droite_nathan()
            self.tirs_gauche_nathan()

            self.explosions_animation_nathan()
            self.sang_de_la_veine_un_nathan()
            self.sang_de_la_veine_deux_nathan()
            if self.combat_final_nathan == True :
                self.background_nathan()

                self.deplacement_plateformes_deux_nathan()
                self.deplacement_plateformes_trois_nathan()
                self.deplacement_plateformes_quatre_nathan()
                self.deplacement_plateformes_cinq_nathan()
                self.deplacement_avec_la_plateforme_nathan()

            #self.kk_touche_nathan()
            self.initialisation_nathan()
            self.enfin_le_boss_nathan()
            self.vaisseau_se_deplace_nathan()

        elif self.vaisseau_sen_va_nathan == True :
            self.cinematique_de_fin_nathan()

    def draw(self):
        if self.vies_nathan>0 :
            self.nbr_vies_nathan = self.vies_nathan // 2
            self.demi_coeur_nathan = self.vies_nathan%2

            self.nbr_coeur_vide_nathan = self.coeur_vide_nathan//2


            for background in self.background_liste_nathan :
                pyxel.bltm(background[0],0,0,0,0,128,128)

            for vaisseau in self.liste_coordonees_vaisseau_nathan :
                pyxel.blt(vaisseau[0],vaisseau[1],0,24,104,8,8,0)


            pyxel.blt(self.xcaca_nathan, self.ycaca_nathan, 0, self.x_sprite_nathan, self.y_sprite_nathan, (self.sens_nathan * 8), 8, 0)


            if self.x_tuyau_nathan>-16 :
                pyxel.blt(self.x_tuyau_nathan,110,0,48,4,14,12,0)

            for kk in range (self.nbr_vies_nathan) :
                pyxel.blt(8+8*kk,8,0,8,104,8,8,0)
            if self.demi_coeur_nathan == 1 :
                pyxel.blt(8+8*self.nbr_vies_nathan,8,0,0,104,8,8,0)
            for kk in range (self.nbr_coeur_vide_nathan) :
                pyxel.blt(8+(8*self.nbr_vies_nathan)+(8*self.demi_coeur_nathan)+(kk*8),8,0,16,104,8,8,0)

            if self.bazooka_nathan == False and self.c_deb_nathan == False:
                if La_kk_venture.Space and self.sens_nathan == 1 :
                    pyxel.blt(self.xcaca_nathan+8, self.ycaca_nathan+3, 0, 16, 3,  8, 8, 0)
                elif La_kk_venture.Space and self.sens_nathan == -1:
                    pyxel.blt(self.xcaca_nathan-8, self.ycaca_nathan+3, 0, 16, 3,  -8, 8, 0)
            elif self.c_deb_nathan == False :
                if self.sens_nathan == 1 :
                    pyxel.blt(self.xcaca_nathan-2,self.ycaca_nathan+4,0,0,114,14,4,0)
                else :
                    pyxel.blt(self.xcaca_nathan-4,self.ycaca_nathan+4,0,0,114,-14,4,0)

            for tir in self.tirs_liste_gauche_nathan :
                pyxel.blt(tir[0],tir[1],0,24,0,-6,3,0)
            for tir in self.tirs_liste_droite_nathan :
                pyxel.blt(tir[0],tir[1],0,24,0,6,3,0)



            if pyxel.frame_count%18>=0 and pyxel.frame_count%18 < 6 :
                self.x_sprite_monstre_un_nathan = 0
                self.x_sprite_monstre_deux_nathan = 0
            elif pyxel.frame_count%18>=6 and pyxel.frame_count%18<12 :
                self.x_sprite_monstre_un_nathan = 8
                self.x_sprite_monstre_deux_nathan = 16
            elif pyxel.frame_count%18>=12 and pyxel.frame_count%18<18 :
                self.x_sprite_monstre_un_nathan = 16
                self.x_sprite_monstre_deux_nathan = 32

            if pyxel.frame_count%2 == 1 :
                if self.sprite_tentacule_nathan > 102 :
                    self.sprite_tentacule_nathan = 52
                else :
                    self.sprite_tentacule_nathan+=8


            for ennemi in self.ennemis_liste_gauche_monstre_un_nathan:
                pyxel.blt(ennemi[0], ennemi[1], 1, self.x_sprite_monstre_un_nathan, 8, 8, 8,0)
            for ennemi in self.ennemis_liste_droite_monstre_un_nathan:
                pyxel.blt(ennemi[0], ennemi[1], 1, self.x_sprite_monstre_un_nathan, 8, -8, 8,0)


            for ennemi in self.ennemis_liste_gauche_monstre_deux_nathan:
                pyxel.blt(ennemi[0], ennemi[1], 1, self.x_sprite_monstre_deux_nathan, 32, 16, 16,0)
            for ennemi in self.ennemis_liste_droite_monstre_deux_nathan:
                pyxel.blt(ennemi[0], ennemi[1], 1, self.x_sprite_monstre_deux_nathan, 32, -16, 16,0)

            for ennemi in self.tir_poulpe_gauche_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1,50,34,4,5,0)
            for ennemi in self.tir_poulpe_droite_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1,50,34,-4,5,0)


            for ennemi in self.tentacule_gauche_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1, 4,self.sprite_tentacule_nathan,12,5,0)
            for ennemi in self.tentacule_droite_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1, 4,self.sprite_tentacule_nathan,-12,5,0)
            for ennemi in self.deplacement_gauche_t_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1, 4,self.sprite_tentacule_nathan,12,5,0)
            for ennemi in self.deplacement_droite_t_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1, 4,self.sprite_tentacule_nathan,-12,5,0)

            if self.en_train_de_tirer_nathan == True :
                for explosion in self.explosions_liste_nathan:
                    pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)
            else :
                for explosion in self.explosions_liste_nathan:
                    pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 2+explosion[2]%3)


            for sange in self.sang_un_nathan :
                pyxel.blt(sange[0],sange[1],0,sange[2],sange[3],8,8,0)
            for sang in self.sang_deux_nathan :
                pyxel.blt(sang[0],sang[1],0,sang[2],16,16,16,0)

            if self.avant_bazooka_nathan== False and self.bazooka_nathan == False and self.boss_nathan==False :
                    pyxel.text(100, 8, str(self.ennemis_killed_nathan) +"/50 ", 7)
            elif self.avant_bazooka_nathan== True and self.bazooka_nathan == False and self.boss_nathan == False :
                pyxel.text(100, 8, str(self.ennemis_killed_nathan) +"/50 ", 10)

            if self.avant_bazooka_nathan == True :
                if pyxel.frame_count%4 <2 :
                    pyxel.text(52, 20, "PRESS F ", 9)
                else :
                    pyxel.text(52, 20, "PRESS F ", 11)

            for ennemi in self.the_B_nathan :
                pyxel.blt(ennemi[0],ennemi[1],1,self.x_sprite_monstre_deux_nathan+16,48,16,16,0)
            if self.laser_nathan == True : # Le laser trop galere a faire...
                if self.Chronodukk%210==151 :
                    pyxel.play(0, 60)
                if self.Chronodukk%210>150 and self.Chronodukk%210<195:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(0*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>152 and self.Chronodukk%210<197:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(1*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>154 and self.Chronodukk%210<199:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(2*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>156 and self.Chronodukk%210<201:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(3*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>158 and self.Chronodukk%210<203:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(4*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>160 and self.Chronodukk%210<205:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(5*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>162 and self.Chronodukk%210<207:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(6*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)
                if self.Chronodukk%210>164 and self.Chronodukk%210<209:
                    pyxel.blt(self.the_B_nathan[0][0]-8+(7*-16),self.the_B_nathan[0][1],1,self.x_sprite_monstre_deux_nathan+16,64,16,16,0)


        else : # si le personnage venait a etre game over, on réinitialise toutes les variables et on relance le jeu
            self.kk_dead_nathan= True
            pyxel.cls(0)
            pyxel.text(50,64, 'GAME OVER', 7)
            pyxel.text(60,74,'RESTART : F',7)
            pyxel.stop()
            La_kk_venture.Press_F = True #Afficher touche F
            if La_kk_venture.F_p :
                pyxel.playm(1,0,True)


                self.Chronodukk = 0
                self.c_deb_nathan = True
                self.attendre_nathan = False
                self.vies_nathan = 20
                self.nbr_vies_nathan = self.vies_nathan // 2
                self.demi_coeur_nathan = self.vies_nathan%2
                self.coeur_vide_nathan = 0
                self.nbr_coeur_vide_nathan = self.coeur_vide_nathan//2

                self.x_tuyau_nathan=0
                self.xcaca_nathan = 0
                self.ycaca_nathan = 112
                self.hspd_nathan = 0
                self.vspd_nathan = 0
                self.size_nathan = 8
                self.sens_nathan = 1
                self.x_sprite_nathan = 0
                self.y_sprite_nathan = 0
                self.isgrounded_nathan = False

                self.liste_plat_un_nathan = [[0, 120, 128, 8]]
                self.liste_plat_deux_nathan=[[14,96,96,8]]
                self.liste_plat_trois_nathan =[[30,72,64,8]]
                self.liste_plat_quatre_nathan=[[47,48,32,8]]
                self.liste_plat_cinq_nathan=[[0,32,24,8],[99,32,24,8]]

                self.tirs_liste_gauche_nathan = []
                self.tirs_liste_droite_nathan = []

                self.ennemis_liste_gauche_monstre_un_nathan=[]
                self.ennemis_liste_droite_monstre_un_nathan=[]

                self.sprite_tentacule_nathan = 51

                self.ennemis_liste_gauche_monstre_deux_nathan=[]
                self.tentacule_gauche_nathan=[]
                self.deplacement_gauche_t_nathan=[]

                self.ennemis_liste_droite_monstre_deux_nathan=[]
                self.tentacule_droite_nathan=[]
                self.deplacement_droite_t_nathan=[]

                self.tir_poulpe_droite_nathan=[]
                self.tir_poulpe_gauche_nathan=[]

                self.x_sprite_monstre_un_nathan = 0
                self.x_sprite_monstre_deux_nathan=0

                self.explosions_liste_nathan=[]
                self.sang_un_nathan=[]
                self.sang_deux_nathan=[]

                self.background_liste_nathan=[[0,0],[127.5,0],[255.5,0]]

                self.avant_bazooka_nathan = False
                self.bazooka_nathan = False
                self.boss_nathan = False
                self.en_train_de_tirer_nathan = False

                self.ennemis_killed_nathan = 0

                self.temps_un_nathan= 400
                self.temps_deux_nathan=1000
                self.explosion_chrono_nathan=60
                self.chrono_boss_nathan = 50
                self.vasy_mon_rey_nathan = False

                self.kk_dead_nathan= False

                self.the_B_nathan= []
                self.combat_final_nathan = False
                self.laser_nathan = False
                self.touche_par_le_boss_nathan = False
                self.couldown_nathan = False
                self.chrono_couldown_nathan =0

                self.vaisseau_sen_va_nathan = False
                self.liste_coordonees_vaisseau_nathan = []


"""
Jeu 4
"""

class Jeu_A:
    def __init__(self):
        pyxel.camera(La_kk_venture.Camera_Buttons,0)
        # chargement des images
        pyxel.load("res_K.pyxres")

        #Lancement de la musique
        pyxel.playm(0,0,True)

        self.cinematique_A = True
        self.cinematique_de_fin_A = False
        self.cest_la_fin = False

        self.x = 64
        self.y = 128
        self.dir_A = 0
        self.dernier_tir_A = 0
        self.tirs_liste_A = []
        self.munitions_A = 10
        self.munitions_epuisees_A = 0
        self.ennemis_liste_A = []

        self.phases_A=[[[Ennemi1, Ennemi2], 10, 2, boss_A1], [[Ennemi3, Ennemi4], 10, 2, boss_A2], [[Ennemi5, Ennemi6], 10, 2, boss_A3], [[Ennemi7, Ennemi8], 10, 2, boss_A4],[[],0,2,boss_A5]]

        self.phase_A=self.phases_A.pop(0)
        self.scroll_y_A = 0
        self.liste_explosions_A = []
        self.pv_A = 17
        self.Chronodukk = 0
        self.final_time_A = 0
        self.game_over_A = False
        self.score_A = 0
        self.niveau_A = 1
        self.game_over_text_A = "GAME OVER"
        self.boss_A=False

    def stop_A(self):
        self.tirs_liste_A = []
        self.ennemis_liste_A = []
        self.liste_explosions_A = []



    def restart_A(self):
        self.Chronodukk = 0
        self.ennemis_liste_A = []
        pyxel.playm(0,0,True)
        self.cinematique_A = True
        self.x = 64
        self.y = 128
        self.dir_A = 0
        self.dernier_tir_A = 0
        self.munitions_A = 10
        self.munitions_epuisees_A = 0
        self.phases_A=[[[Ennemi1, Ennemi2], 10, 2, boss_A1], [[Ennemi3, Ennemi4], 10, 2, boss_A2], [[Ennemi5, Ennemi6], 10, 2, boss_A3], [[Ennemi7, Ennemi8], 10, 2, boss_A4],[[],0,2,boss_A5]]
        self.phase_A=self.phases_A.pop(0)
        self.scroll_y_A = 0
        self.pv_A = 17
        self.final_time_A = 0
        self.game_over_A = False
        self.score_A = 0
        self.niveau_A = 1
        self.boss_A=False

        self.cinematique_A = True
        self.cinematique_de_fin_A = False
        self.cest_la_fin = False



    def cinematique_debut_A(self):
        if self.y >64 :
            self.y-=1
        else :
            self.cinematique_A = False

    def faire_la_cinematique_de_fin(self) :
        if self.y>-16 :
            self.y-=1
        else :
            self.y=128
            self.cest_la_fin = True
            self.cinematique_de_fin_A = False
            pyxel.stop()
            pyxel.playm(1,0,False)


    #Création des Mouvements avec les flèches dir_Aectionnelles
    def mvt_A(self):
        if La_kk_venture.Left and self.x > 0:
            self.x -= 3
            self.dir_A = 1
        elif La_kk_venture.Right and self.x < 120:
            self.x += 3
            self.dir_A = 1
        else:
            self.dir_A = 0
        if La_kk_venture.Up and self.y > 24:
            self.y -= 3
        if La_kk_venture.Down and self.y < 112:
            self.y += 3


    #Création des tirs
    def creer_tir_A(self):
        if pyxel.frame_count-self.dernier_tir_A >= 4 and self.munitions_A:
            self.dernier_tir_A = pyxel.frame_count
            self.tirs_liste_A.append([self.x, self.y])
            self.munitions_A -= 1
            if self.munitions_A == 0:
                self.munitions_epuisees_A = pyxel.frame_count

    #Vitesse du tir
    def avancer_tir_A(self):
        for tir in self.tirs_liste_A:
            tir[1] -= 5

    #Création des Ennemies a un emplacement random
    def creer_ennemi_A(self, ennemi):
        self.ennemis_liste_A.append(ennemi(random.randint(0, 120), 24, self))

    #Vérification des collisions du tir sur les Ennemies
    def verifier_collisions_tirs_A(self):
        for ennemi in self.ennemis_liste_A:
            for tir in self.tirs_liste_A:
                if -8 < tir[0]-ennemi.x < ennemi.w and -8 < ennemi.y-tir[1] < ennemi.h:
                    ennemi.pv_A -= self.niveau_A
                    self.score_A+=10
                    if ennemi.pv_A <= 0:
                        pyxel.play(3, 2)
                        #Si Ennemie dead, Bruitage
                        self.score_A+=10
                        self.liste_explosions_A.append(
                            [ennemi.x, ennemi.y, 1, 0])
                    self.tirs_liste_A.remove(tir)


    #Vérification collisions des Ennemies sur le Vaisseau
    def verifier_collisions_joueur_A(self):
        for ennemi in self.ennemis_liste_A:
            if -8 < ennemi.x-self.x < ennemi.w and -8 < ennemi.y-self.y < ennemi.h:
                self.pv_A -= ennemi.pv_A
                self.liste_explosions_A.append([ennemi.x, ennemi.y, 1, 0])
                ennemi.existe_A = 0
                if self.pv_A <= 0:
                    self.liste_explosions_A.append([self.x, self.y, 0, 0])
            for tir in ennemi.tirs_liste_A:
                if -8 < self.x-(tir[0]+3) < 2 and -2 < self.y-(tir[1]+3) < 8:
                    self.pv_A -= tir[2]+1
                    pyxel.play(3, 1)
                    #Si Vaisseau toucher, Bruitage
                    ennemi.tirs_liste_A.remove(tir)
                    if self.pv_A <= 0:
                        pyxel.play(3, 3)
                        #Si Vaisseau dead, Bruitage
                        self.stop_A()
                        self.liste_explosions_A.append([self.x, self.y, 0, 0])


    def update(self):
        self.Chronodukk += 1

        if self.cinematique_A == True:
            self.cinematique_debut_A()

        elif self.cinematique_de_fin_A == False and self.cest_la_fin == False:


            if self.game_over_A:
                return

            self.scroll_y_A = (self.scroll_y_A+1) % 1024
            self.mvt_A()

            if La_kk_venture.Space:
                self.creer_tir_A()
            self.avancer_tir_A()

            if self.munitions_A == 0 and (pyxel.frame_count-self.munitions_epuisees_A) % 30 == 29:
                self.munitions_A = 10

            if not self.boss_A:
                if self.phase_A[1]==0:
                    if not self.ennemis_liste_A:
                        self.boss_A=True
                        self.creer_ennemi_A(self.phase_A[3])
                        if self.phases_A: self.phase_A=self.phases_A.pop(0)

                elif pyxel.frame_count % (30*self.phase_A[2]) == 0:
                    self.creer_ennemi_A(random.choice(self.phase_A[0]))
                    self.phase_A[1]-=1
            self.verifier_collisions_tirs_A()
            self.verifier_collisions_joueur_A()

            for ennemi in self.ennemis_liste_A:
                if not ennemi.existe_A:
                    self.ennemis_liste_A.remove(ennemi)
                else:
                    ennemi.update_A()

            if self.pv_A <= 0 and not self.liste_explosions_A:
                self.game_over_A = True
                self.final_time_A=temps_A(self.Chronodukk)


        elif self.cinematique_de_fin_A == True :
            self.faire_la_cinematique_de_fin()



        elif self.cest_la_fin == True :
            La_kk_venture.Press_F = True #Afficher touche F
            if La_kk_venture.F_p :
                La_kk_venture.Jeu = 1
                La_kk_venture.Initialisation = True

    def draw(self):
        pyxel.cls(0)
        if self.game_over_A:

            pyxel.stop()
            #pyxel.mouse(True)

            pyxel.text(45, 55, f"{self.game_over_text_A}\nscore {self.score_A}\nTIME  {self.final_time_A}", 7)
            pyxel.text(33, 75, f"Press F to restart", 5)

            self.stop_A()
            La_kk_venture.Press_F = True #Afficher touche F
            if La_kk_venture.F_p:
                #pyxel.mouse(False)
                self.restart_A()
            return
        elif self.cest_la_fin == False :
            etat_A = pyxel.frame_count % 3
            pyxel.bltm(0, self.scroll_y_A, 0, 0, 128, 128, 8*128)
            pyxel.bltm(0, self.scroll_y_A-1024-128, 0, 0, 0, 128, 8*128)
            pyxel.blt(self.x, self.y, 0, 8*self.dir_A, 8, 8, 8, 0)
            pyxel.blt(self.x, self.y+8, 0, 8*etat_A, 0, 8, 8, 0)

            if self.cinematique_de_fin_A == False :
                for tir in self.tirs_liste_A:
                    pyxel.blt(tir[0], tir[1], 0, 0, 24+(self.niveau_A-1)*8, 8, 8, 0)

                for ennemi in self.ennemis_liste_A:
                    pyxel.blt(ennemi.x, ennemi.y, 0, ennemi.tile_x,
                        ennemi.tile_y+ennemi.etat_A*8, ennemi.w, ennemi.h, 0)

                    for tir in ennemi.tirs_liste_A:
                        pyxel.blt(tir[0], tir[1], 0, 8+8*(tir[2] %
                            2), 16+8*(tir[2]//2), 8, 8, 0)

                for explosion in self.liste_explosions_A:
                    pyxel.blt(explosion[0], explosion[1], 0, 8+8 *
                        explosion[2], 128+8*explosion[3], 8, 8, 0)
                    explosion[3] += 1
                    if explosion[3] > 2:
                        self.liste_explosions_A.remove(explosion)



            #Coordonnées du grand cadre en haut
            pyxel.blt(0, 0, 0, 0, 104, 128, 24)
            #Affichage de la barre de vie
            pyxel.line(46, 10, 46, 12, 14)
            pyxel.line(47, 9, 46+2*self.pv_A, 9, 14)
            pyxel.rect(47, 10, self.pv_A*2, 3, 8)
            pyxel.line(47, 13, 46+2*self.pv_A, 13, 14)
            pyxel.line(47+2*self.pv_A, 10, 47+2*self.pv_A, 12, 14)
            #Affichage de l'image des munitions_A
            pyxel.blt(10, 8, 0, 0,8*(self.niveau_A-1)+ 24, 8, 8)
            #Affichage du nombre de munitions_A restantes
            pyxel.text(20, 9, f"x{self.munitions_A}", 7)
            #Affichage du score_A
            pyxel.text(100, 9, str(self.score_A), 7)
            #Affichage du temps_A qui passe
            pyxel.text(1, 120, temps_A(self.Chronodukk), 7)







        elif self.cest_la_fin == True :

            pyxel.bltm(0,0,1,0,0,128,128)

            pyxel.text(10, 110, "PRESS F TO RESTART", 10)
            pyxel.text(59, 13, "FIN ", 0)

#Autres class
# Minuteur
def temps_A(frames):
    frames=frames/30
    s=frames%60
    min= frames//60
    return f"{int(min):01}:{int(s):02}"


#Création des positions, pv des Ennemis
class Ennemi_A:

    def __init__(self, tile_x, tile_y, h, w, x, y, pv_A, jeu_A):
        self.x = x
        self.y = y
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.h = h
        self.w = w
        self.existe_A = True
        self.etat_A = 0
        self.pv_A = pv_A
        self.tirs_liste_A = []
        self.jeu_A = jeu_A

    #Création des tirs
    def creer_tir_A(self, type):
        self.tirs_liste_A.append([self.x+(self.w-2)/2, self.y+0.7*self.h, type])

    #Mise a Jour des tirs
    def update_A_tirs(self, vitesse):
        for tir in self.tirs_liste_A:
            tir[1] += vitesse


#Création des actions des Ennemies
class Ennemi1(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(24, 8, 8, 8, x, y, 1, jeu_A)

    #Mise a Jour de l'Ennmie
    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(60) == 0:
            self.creer_tir_A(0)
        self.update_A_tirs(2)
        self.y += 0.25
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi2(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(32, 8, 8, 8, x, y, 2, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(60) == 0:
            self.creer_tir_A(1)
        self.update_A_tirs(3)
        self.y += 0.25
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False


class Ennemi3(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(40, 8, 8, 8, x, y, 2, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(60) == 0:
            self.creer_tir_A(3)
        self.update_A_tirs(4)
        self.y += 0.1
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi4(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(48, 8, 8, 8, x, y, 3, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(60) == 0:
            self.creer_tir_A(4)
        self.update_A_tirs(4)
        self.y += 0.25
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi5(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(56, 8, 8, 8, x, y, 1, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(30) == 0:
            self.creer_tir_A(6)
        self.update_A_tirs(5)
        self.y += 0.4
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi6(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(64, 8, 8, 8, x, y, 6, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(60) == 0:
            self.creer_tir_A(7)
        self.update_A_tirs(5)
        self.y += 0.2
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi7(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(72, 8, 8, 8, x, y, 4, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(30) == 0:
            self.creer_tir_A(8)
        self.update_A_tirs(5)
        self.y += 0.15
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False

class Ennemi8(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(80, 8, 8, 8, x, y, 7, jeu_A)

    def update_A(self):
        if pyxel.frame_count % 20 >= 10:
            self.etat_A = 1
        else:
            self.etat_A = 0
        if random.randrange(90) == 0:
            self.creer_tir_A(9)
        self.update_A_tirs(5)
        self.y += 0.15
        if self.y > 128 or self.pv_A <= 0:
            self.existe_A = False





#Création des actions des boss_A
class boss_A1(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(24, 24, 16, 16, x, y, 20, jeu_A)

    def update_A(self):
        if self.x+4<self.jeu_A.x:
            self.x+=0.5
        elif self.x+4>self.jeu_A.x:
            self.x-=0.5
        if random.randrange(60) == 0:
            self.creer_tir_A(2)
        self.update_A_tirs(2)
        if self.pv_A <= 0:
            self.existe_A = False
            self.jeu_A.niveau_A+=1
            #Ameliore le Missile
            self.jeu_A.boss_A=False

class boss_A2(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(40, 24, 24, 16, x, y, 40, jeu_A)

    def update_A(self):

        if self.x+4<self.jeu_A.x:
            self.x+=0.5
        elif self.x+4>self.jeu_A.x:
            self.x-=0.5
        if random.randrange(40) == 0:
            self.creer_tir_A(5)
        self.update_A_tirs(3)


        if self.pv_A <= 0:
            self.existe_A = False
            self.jeu_A.niveau_A+=1
            self.jeu_A.boss_A=False

class boss_A3(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(56, 24, 24, 16, x, y, 40, jeu_A)

    def update_A(self):

        if self.x+4<self.jeu_A.x:
            self.x+=0.5
        elif self.x+4>self.jeu_A.x:
            self.x-=0.5
        if random.randrange(60) == 0:
            self.creer_tir_A(10)
        self.update_A_tirs(5)


        if self.pv_A <= 0:
            self.existe_A = False
            self.jeu_A.niveau_A+=1
            self.jeu_A.boss_A=False

class boss_A4(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(72, 24, 16, 16, x, y, 60, jeu_A)

    def update_A(self):

        if self.x+4<self.jeu_A.x:
            self.x+=0.5
        elif self.x+4>self.jeu_A.x:
            self.x-=0.5
        if random.randrange(20) == 0:
            self.creer_tir_A(11)
        self.update_A_tirs(5)


        if self.pv_A <= 0:
            self.existe_A = False
            self.jeu_A.niveau_A+=1
            self.jeu_A.boss_A=False

class boss_A5(Ennemi_A):
    def __init__(self, x, y, jeu_A):
        super().__init__(40, 48, 24, 32, x, y, 100, jeu_A)

    def update_A(self):

        if self.x+12<self.jeu_A.x:
            self.x+=0.5
        elif self.x+12>self.jeu_A.x:
            self.x-=0.5
        if random.randrange(30) == 0:
            self.creer_tir_A(12)
        self.update_A_tirs(7)


        if self.pv_A <= 0:
            self.existe_A = False
            self.jeu_A.cinematique_de_fin_A = True
            #self.jeu_A.game_over_A=True
            self.jeu_A.game_over_text_A="Bien Joue !!"
            #self.jeu_A.final_time_A = temps_A(pyxel.frame_count)



"""
Jeu La kk-venture
"""


class La_kk_venture_class:
    def init(self):
        pyxel.init(256, 128, title="La_kk_venture", fps=30)
        self.Jeu = 1
        self.Initialisation = True
        self.Camera_Buttons = -64
        self.Cursor_x = 0
        self.Cursor_y = 0
        self.J_p = False
        self.K_p = False
        self.Choix = False
        self.Press_F = False

        #Choix du mode
        self.On_Mobile = False


        pyxel.run(self.update, self.draw)

    def coords_in(self, mouse_x, mouse_y, x, y, taille_h, taille_v):
        if (mouse_x > x and mouse_x < x+taille_h) and (mouse_y > y and mouse_y < y+taille_v):
            return True
        return False

    def update_Buttons(self,x,y):
        if self.On_Mobile: #Si le mode Mobile est choisi
            #Bontons
            self.mouse_p = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            self.mouse = pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
            #Space
            self.Space_p = pyxel.btnp(pyxel.KEY_SPACE) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+96, 64, 32))
            self.Space = pyxel.btn(pyxel.KEY_SPACE) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+96, 64, 32))
            #Left
            self.Left = pyxel.btn(pyxel.KEY_LEFT) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+0, y+96, 32, 32))
            #Right
            self.Right = pyxel.btn(pyxel.KEY_RIGHT) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+32, y+96, 32, 32))
            #Up
            self.Up_p = pyxel.btnp(pyxel.KEY_UP) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+64, 32, 32))
            self.Up = pyxel.btn(pyxel.KEY_UP) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+64, 32, 32))
            #Down
            self.Down_p = pyxel.btnp(pyxel.KEY_DOWN) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+224, y+64, 32, 32))
            self.Down = pyxel.btn(pyxel.KEY_DOWN) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+224, y+64, 32, 32))
            #A
            self.A_p = pyxel.btnp(pyxel.KEY_A) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+0, y+32, 32, 32))
            self.A = pyxel.btn(pyxel.KEY_A) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+0, y+32, 32, 32))
            #B
            self.B_p = pyxel.btnp(pyxel.KEY_B) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+32, y+32, 32, 32))
            self.B = pyxel.btn(pyxel.KEY_B) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+32, y+32, 32, 32))
            #F
            self.F_p = pyxel.btnp(pyxel.KEY_F) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+0, y+0, 32, 32))
            self.F = pyxel.btn(pyxel.KEY_F) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+0, y+0, 32, 32))
            #J
            self.J_p = pyxel.btnp(pyxel.KEY_J) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+0, 32, 32))
            self.J = pyxel.btn(pyxel.KEY_J) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+192, y+0, 32, 32))
            #K
            self.K_p = pyxel.btnp(pyxel.KEY_K) or (self.mouse_p and self.coords_in(self.Cursor_x, self.Cursor_y, x+224, y+0, 32, 32))
            self.K = pyxel.btn(pyxel.KEY_K) or (self.mouse and self.coords_in(self.Cursor_x, self.Cursor_y, x+224, y+0, 32, 32))
        else: #Mode Clavier
            #Bontons
            #Space
            self.Space_p = pyxel.btnp(pyxel.KEY_SPACE)
            self.Space = pyxel.btn(pyxel.KEY_SPACE)
            #Left
            self.Left = pyxel.btn(pyxel.KEY_LEFT)
            #Right
            self.Right = pyxel.btn(pyxel.KEY_RIGHT)
            #Up
            self.Up_p = pyxel.btnp(pyxel.KEY_UP)
            self.Up = pyxel.btn(pyxel.KEY_UP)
            #Down
            self.Down_p = pyxel.btnp(pyxel.KEY_DOWN)
            self.Down = pyxel.btn(pyxel.KEY_DOWN)
            #A
            self.A_p = pyxel.btnp(pyxel.KEY_A)
            self.A = pyxel.btn(pyxel.KEY_A)
            #B
            self.B_p = pyxel.btnp(pyxel.KEY_B)
            self.B = pyxel.btn(pyxel.KEY_B)
            #F
            self.F_p = pyxel.btnp(pyxel.KEY_F)
            self.F = pyxel.btn(pyxel.KEY_F)
            #J
            self.J_p = pyxel.btnp(pyxel.KEY_J)
            self.J = pyxel.btn(pyxel.KEY_J)
            #K
            self.K_p = pyxel.btnp(pyxel.KEY_K)
            self.K = pyxel.btn(pyxel.KEY_K)


    def draw_Buttons(self, x, y, index_de_l_image):
        if self.On_Mobile: #Si le mode Mobile est choisi
            if self.Jeu != 2: #Si pas jeu Damien
                #Left
                if self.Left : pyxel.blt(x, y+96, index_de_l_image, 0, 64, 32, 32)
                else: pyxel.blt(x, y+96, index_de_l_image, 0, 0, 32, 32)
                #Right
                if self.Right : pyxel.blt(x+32, y+96, index_de_l_image, 32, 64, 32, 32)
                else: pyxel.blt(x+32, y+96, index_de_l_image, 32, 0, 32, 32)
                #Up
                if self.Up : pyxel.blt(x+192, y+64, index_de_l_image, 64, 64, 32, 32)
                else: pyxel.blt(x+192, y+64, index_de_l_image, 64, 0, 32, 32)
                #Down
                if self.Down : pyxel.blt(x+224, y+64, index_de_l_image, 64, 96, 32, 32)
                else: pyxel.blt(x+224, y+64, index_de_l_image, 64, 32, 32, 32)
            #Space
            if self.Space : pyxel.blt(x+192, y+96, index_de_l_image, 0, 96, 64, 32)
            else: pyxel.blt(x+192, y+96, index_de_l_image, 0, 32, 64, 32)
            if self.Choix:
                #A
                if self.A : pyxel.blt(x, y+32, index_de_l_image, 96, 64, 32, 32)
                else: pyxel.blt(x, y+32, index_de_l_image, 96, 0, 32, 32)
                #B
                if self.B : pyxel.blt(x+32, y+32, index_de_l_image, 96, 96, 32, 32)
                else: pyxel.blt(x+32, y+32, index_de_l_image, 96, 32, 32, 32)
            if self.Press_F:
                #F
                if self.F : pyxel.blt(x+0, y+0, index_de_l_image, 160, 64, 32, 32)
                else: pyxel.blt(x+0, y+0, index_de_l_image, 160, 0, 32, 32)
            #J
            if self.J : pyxel.blt(x+192, y+0, index_de_l_image, 128, 64, 32, 32)
            else: pyxel.blt(x+192, y+0, index_de_l_image, 128, 0, 32, 32)
            #K
            if self.K : pyxel.blt(x+224, y+0, index_de_l_image, 128, 96, 32, 32)
            else: pyxel.blt(x+224, y+0, index_de_l_image, 128, 32, 32, 32)

    def update(self):
        #Pouvoir contrôler les jeux
        if self.J_p:
            if self.Jeu == 1:
                self.Initialisation = True
                pyxel.stop()
            else:
                self.Jeu -= 1
                self.Initialisation = True
                pyxel.stop()
        if self.K_p:
            if self.Jeu == 4:
                self.Initialisation = True
                pyxel.stop()
            else:
                self.Jeu += 1
                self.Initialisation = True
                pyxel.stop()

        #Initialisation de chaque jeu
        if self.Initialisation == True:
            if self.Jeu == 1 :
                self.Jeu_Er_kk = Jeu_Er()
                self.Initialisation = False
            elif self.Jeu == 2 :
                self.Jeu_D_kk = Jeu_D()
                self.Initialisation = False
            elif self.Jeu == 3 :
                self.Jeu_N_kk = Jeu_N()
                self.Initialisation = False
            elif self.Jeu == 4 :
                self.Jeu_A_kk = Jeu_A()
                self.Initialisation = False

                #Curseur
        if self.Jeu == 2:
            self.Cursor_x = pyxel.mouse_x+self.Camera_Buttons+self.Jeu_D_kk.xcam+self.Jeu_D_kk.speed
            self.Cursor_y = pyxel.mouse_y+self.Jeu_D_kk.ycam
        else:
            self.Cursor_x = pyxel.mouse_x+self.Camera_Buttons
            self.Cursor_y = pyxel.mouse_y

        #Boutons
        if self.Jeu == 2: #Si jeu Damien
            self.update_Buttons(self.Jeu_D_kk.xcam+self.Camera_Buttons, self.Jeu_D_kk.ycam)
        else:
            self.update_Buttons(0+self.Camera_Buttons,0)

        #Arrêter l'affichage des boutons
        self.Choix = False
        self.Press_F = False

        #Update de chaque jeu
        if self.Jeu == 1 :
            self.Jeu_Er_kk.update()
        elif self.Jeu == 2 :
            self.Jeu_D_kk.update()
        elif self.Jeu == 3 :
            self.Jeu_N_kk.update()
        elif self.Jeu == 4 :
            self.Jeu_A_kk.update()

    #Draw de chaque jeu
    def draw(self):
        if self.Jeu == 1 and self.Initialisation == False:
            self.Jeu_Er_kk.draw()
        elif self.Jeu == 2 and self.Initialisation == False:
            self.Jeu_D_kk.draw()
        elif self.Jeu == 3 and self.Initialisation == False:
            self.Jeu_N_kk.draw()
        elif self.Jeu == 4 and self.Initialisation == False:
            self.Jeu_A_kk.draw()


        #Pour boutons
        if self.Jeu == 2 and self.Initialisation == False: #Si jeu Damien, boîte aux bonnes coordonnées par rapport à camera
            if self.Jeu_D_kk.Cin_begin == False: #Si n'est pas dans la cinématique de fin
                if self.Jeu_D_kk.Cin_end == 1:
                    pyxel.rect(40*8+self.Camera_Buttons, 96*8, -self.Camera_Buttons, 128, 0)
                    pyxel.rect(40*8+128, 96*8, -self.Camera_Buttons, 128, 0)
                    self.draw_Buttons(40*8+self.Camera_Buttons, 96*8, 1)
                elif self.Jeu_D_kk.Cin_end == 2:
                    pyxel.rect(56*8+self.Camera_Buttons, 96*8, -self.Camera_Buttons, 128, 0)
                    pyxel.rect(56*8+128, 96*8, -self.Camera_Buttons, 128, 0)
                    self.draw_Buttons(56*8+self.Camera_Buttons, 96*8, 1)
                else:
                    pyxel.rect(self.Jeu_D_kk.xcam+self.Camera_Buttons, self.Jeu_D_kk.ycam, -self.Camera_Buttons, 128, 0)
                    pyxel.rect(self.Jeu_D_kk.xcam+128, self.Jeu_D_kk.ycam, -self.Camera_Buttons, 128, 0)
                    self.draw_Buttons(self.Jeu_D_kk.xcam+self.Camera_Buttons, self.Jeu_D_kk.ycam, 1)

                    if pyxel.btnp(pyxel.KEY_F):
                        self.Jeu_D_kk.x = 39*8
                        self.Jeu_D_kk.y = 97*8

        else: #Sinon, même coordonnées pour les autres jeu
            pyxel.rect(self.Camera_Buttons, 0, -self.Camera_Buttons, 128, 0)
            pyxel.rect(128, 0, -self.Camera_Buttons, 128, 0)

            if self.Jeu == 3: #Si jeu de Nathan, changer l'index
                self.draw_Buttons(0+self.Camera_Buttons, 0, 2)
            else:
                if self.Jeu == 4 and self.Initialisation == True: #Fixe bug Transition Nathan -> Adam
                    self.draw_Buttons(0+self.Camera_Buttons, 0, 2)
                else:
                    self.draw_Buttons(0+self.Camera_Buttons, 0, 1)





La_kk_venture = La_kk_venture_class()
La_kk_venture.init()
