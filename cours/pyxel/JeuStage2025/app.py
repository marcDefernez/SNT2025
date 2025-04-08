import pyxel
import random
    
 # Configuration du jeu
WINDOW_WIDTH = 128
WINDOW_HEIGHT = 128
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 3
PLATFORM_WIDTH = 20
PLATFORM_HEIGHT = 5
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 3
GRAVITY = 0.2
JUMP_STRENGTH = -5.5
MAX_FALL_SPEED = 3  # Limiter la vitesse de chute maximale
debounce = 10
ennemy_sprite = True
star_sprite = True
star_debounce = 20

class ClimberGame:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Climber")
        
        self.reset_game()
        pyxel.load("res.pyxres")
        self.game_over = False
        pyxel.playm(0,loop=True)
        pyxel.run(self.update, self.draw)

    def reset_game(self, keep_score=False):
        # Si on garde le score, alors on ne rÃ©initialise que la position du joueur et les plateformes
        if not keep_score:
            self.score = 0
            self.lives = 800 # Nombre de vies initial
        
        # Plateforme de dÃ©part en bas de l'Ã©cran (la premiÃ¨re plateforme)
        start_platform_x = WINDOW_WIDTH // 2 - PLATFORM_WIDTH // 2
        start_platform_y = WINDOW_HEIGHT - PLATFORM_HEIGHT - 10
        self.platforms = [(start_platform_x, start_platform_y)]
        
        # Positionner le joueur centrÃ© sur la premiÃ¨re plateforme
        self.player_x = start_platform_x + PLATFORM_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_y = start_platform_y - PLAYER_HEIGHT
        self.player_dy = 0
        self.on_ground = True

        # Ajout de plateformes supplÃ©mentaires et d'étoiles pour le reste de l'Ã©cran
        self.stars = [(random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH), i * 40) for i in range(1, 8)]
        self.platforms += [
            (random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH), i * 30 + 30)
            for i in range(1, 5)
        ]

        # Ennemis : placer les ennemis initialement en haut avec une direction alÃ©atoire
        self.enemies = [(random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH), i * 40) for i in range(1, 4)]
        self.enemy_directions = [random.choice([-1, 1]) for _ in self.enemies]  # Direction de chaque ennemi (-1 pour gauche, 1 pour droite)

        # DÃ©calage vertical pour simuler le dÃ©filement
        self.scroll_offset = 0

        # RÃ©initialiser le flag de "Game Over"
        self.game_over = False

    def update(self):
        if self.game_over:
            # RÃ©initialiser le jeu si Game Over et la touche R est pressÃ©e
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        self.update_player()
        self.update_enemies()
        self.check_collisions()

        # Si le joueur dÃ©passe la moitiÃ© de l'Ã©cran en hauteur, dÃ©caler le dÃ©cor
        if self.player_y < WINDOW_HEIGHT // 2:
            self.scroll_offset += 2
            self.player_y += 1  # Ajuster lÃ©gÃ¨rement le joueur pour simuler l'ascension continue
            self.score += 1  # Augmenter le score lorsqu'on avance dans le jeu

            # DÃ©placer les plateformes et ennemis vers le bas
            self.platforms = [(x, y + 1) for x, y in self.platforms]
            self.enemies = [(ex, ey + 1) for ex, ey in self.enemies]
            self.stars = [(ex, ey + 1) for ex, ey in self.stars]

            # Supprimer les plateformes en bas et en ajouter en haut
            self.platforms = [
                (x, y) for x, y in self.platforms if y < WINDOW_HEIGHT
            ]
            self.stars = [
                (x, y) for x, y in self.stars if y < WINDOW_HEIGHT
            ]
            while len(self.stars) < 3:
                new_enemy_y = min(ey for _, ey in self.stars) - 40 if self.stars else 0
                new_enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
                self.stars.append((new_enemy_x, new_enemy_y))
                
                
            if len(self.platforms) < 5:
                new_platform_y = min(y for _, y in self.platforms) - 30
                new_platform_x = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)
                self.platforms.append((new_platform_x, new_platform_y))

            # Supprimer les ennemis en bas et en ajouter en haut
            self.enemies = [
                (ex, ey) for ex, ey in self.enemies if ey < WINDOW_HEIGHT
            ]
            while len(self.enemies) < 3:
                new_enemy_y = min(ey for _, ey in self.enemies) - 60 if self.enemies else 0
                new_enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
                self.enemies.append((new_enemy_x, new_enemy_y))
                self.enemy_directions.append(random.choice([-1, 1]))

    def update_player(self):
        # DÃ©placement horizontal
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2
        
        if pyxel.btn(pyxel.KEY_DOWN) and not self.on_ground :
            print("stop")
            self.player_dy += GRAVITY

        # Appliquer la gravitÃ© uniquement si le joueur n'est pas au sol
        if not self.on_ground:
            self.player_dy += GRAVITY
            # Limiter la vitesse de chute maximale
            if self.player_dy > MAX_FALL_SPEED:
                self.player_dy = MAX_FALL_SPEED
            self.player_y += self.player_dy

        # Saut : Si le joueur est sur le sol, il peut sauter
        if self.on_ground and pyxel.btnp(pyxel.KEY_SPACE):
            self.player_dy = JUMP_STRENGTH
            pyxel.play(2,0)
            self.on_ground = False

        # Garder le joueur dans les limites de l'Ã©cran
        self.player_x = max(0, min(WINDOW_WIDTH - PLAYER_WIDTH, self.player_x))
        self.player_y = min(WINDOW_HEIGHT - PLAYER_HEIGHT, self.player_y)

        # Si le joueur tombe en bas de l'Ã©cran
        if self.player_y >= WINDOW_HEIGHT - PLAYER_HEIGHT :
            self.lives -= 1
            if self.lives > 0:
                pyxel.play(1,1)
                self.reset_game(keep_score=True)  # Garde le score et enlÃ¨ve une vie
            else:
                self.game_over = True

    def update_enemies(self):
        global debounce
        global ennemy_sprite
        global star_sprite
        global star_debounce
        debounce = debounce - 1
        star_debounce = star_debounce - 1
        if debounce <= 0:

            debounce += 10
            ennemy_sprite = (not ennemy_sprite)
        if star_debounce <= 0:

            star_debounce += 20
            star_sprite = (not star_sprite)

            
        for i, (ex, ey) in enumerate(self.enemies):
            # DÃ©placer chaque ennemi dans sa direction
            direction = self.enemy_directions[i]

            ex += direction

            # Changer de direction si l'ennemi atteint les bords de l'Ã©cran
            if ex <= 0:
                ex = 0
                self.enemy_directions[i] = 1  # Tourner vers la droite
            elif ex >= WINDOW_WIDTH - ENEMY_WIDTH:
                ex = WINDOW_WIDTH - ENEMY_WIDTH
                self.enemy_directions[i] = -1  # Tourner vers la gauche

            self.enemies[i] = (ex, ey)

    def check_collisions(self):
        # RÃ©initialiser `self.on_ground` pour vÃ©rifier s'il est en contact avec une plateforme
        self.on_ground = False
        for (px, py) in self.platforms:
            # VÃ©rifier la collision entre le joueur et la plateforme
            if (
                self.player_x + PLAYER_WIDTH > px
                and self.player_x < px + PLATFORM_WIDTH
                and self.player_y + PLAYER_HEIGHT <= py  # Le joueur est juste au-dessus de la plateforme
                and self.player_y + PLAYER_HEIGHT + self.player_dy >= py  # Le joueur tombe vers la plateforme
                and self.player_dy >= 0  # La vitesse verticale est dirigÃ©e vers le bas ou nulle
            ):
                # Ajuster la position du joueur juste au-dessus de la plateforme
                self.player_y = py - PLAYER_HEIGHT
                self.player_dy = 0  # ArrÃªter la gravitÃ© (vitesse verticale)
                self.on_ground = True
                break  # Sortir de la boucle aprÃ¨s avoir dÃ©tectÃ© une collision

        # VÃ©rification de collision avec les ennemis
        for (ex, ey) in self.enemies:
            if (
                self.player_x < ex + ENEMY_WIDTH
                and self.player_x + PLAYER_WIDTH > ex
                and self.player_y < ey + ENEMY_HEIGHT
                and self.player_y + PLAYER_HEIGHT > ey
            ):
                # En cas de collision, le joueur perd une vie
                self.lives -= 1
                if self.lives > 0:
                    pyxel.play(1,1)
                    self.reset_game(keep_score=True)
                else:
                    self.game_over = True

    def draw(self):
        pyxel.cls(0)
        # Dessiner le joueur
        if self.on_ground:
            pyxel.blt(self.player_x, self.player_y, 0 , 4, 5, 8, 3, 0)
        else:
            pyxel.blt(self.player_x, self.player_y, 0 , 28, 5, 8, 4, 0)
        
        # Dessiner les plateformes
        for (px, py) in self.platforms:
            pyxel.blt(px, py, 0 , 0, 8, PLATFORM_WIDTH+1, PLATFORM_HEIGHT, 0)
        for i,(ex, ey) in enumerate(self.stars):
            if star_sprite == True:
                pyxel.blt(ex, ey, 0 , 21, 13, 5, 5, 0)
            else:
                pyxel.blt(ex, ey, 0 , 27, 13, 5, 5, 0)
        # Dessiner les ennemis (oiseaux)
        for i,(ex, ey) in enumerate(self.enemies):
            
            if ennemy_sprite == True:
                if self.enemy_directions[i] == -1:
                    
                    pyxel.blt(ex, ey, 0 , 9, 14, ENEMY_WIDTH, ENEMY_HEIGHT, 0)
                else:
                    pyxel.blt(ex, ey, 0 , 0, 14, ENEMY_WIDTH, ENEMY_HEIGHT, 0)
            else:
                if self.enemy_directions[i] == -1:
                    
                    pyxel.blt(ex, ey, 0 , 9, 18, ENEMY_WIDTH, ENEMY_HEIGHT, 0)
                else:
                    pyxel.blt(ex, ey, 0 , 0, 18, ENEMY_WIDTH, ENEMY_HEIGHT, 0)

        # Afficher le score, les vies et instructions
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Vies: {self.lives}", 7)
        

        # Afficher Game Over si le joueur n'a plus de vies
        if self.game_over:
            pyxel.text(40, 60, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(20, 70, "Appuyez sur R pour rejouer", pyxel.COLOR_WHITE)

# Lancer le jeu
ClimberGame()