import pyxel
import random
    
 # Configuration du jeu
WINDOW_WIDTH = 128
WINDOW_HEIGHT = 128
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLATFORM_WIDTH = 20
PLATFORM_HEIGHT = 5
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
GRAVITY = 0.2
JUMP_STRENGTH = -5.5
MAX_FALL_SPEED = 3  # Limiter la vitesse de chute maximale

class ClimberGame:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Climber")
        self.reset_game()
        self.game_over = False
        pyxel.run(self.update, self.draw)

    def reset_game(self, keep_score=False):
        # Si on garde le score, alors on ne réinitialise que la position du joueur et les plateformes
        if not keep_score:
            self.score = 0
            self.lives = 3  # Nombre de vies initial
        
        # Plateforme de départ en bas de l'écran (la première plateforme)
        start_platform_x = WINDOW_WIDTH // 2 - PLATFORM_WIDTH // 2
        start_platform_y = WINDOW_HEIGHT - PLATFORM_HEIGHT - 10
        self.platforms = [(start_platform_x, start_platform_y)]
        
        # Positionner le joueur centré sur la première plateforme
        self.player_x = start_platform_x + PLATFORM_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_y = start_platform_y - PLAYER_HEIGHT
        self.player_dy = 0
        self.on_ground = True

        # Ajout de plateformes supplémentaires pour le reste de l'écran
        self.platforms += [
            (random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH), i * 30 + 30)
            for i in range(1, 5)
        ]

        # Ennemis : placer les ennemis initialement en haut avec une direction aléatoire
        self.enemies = [(random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH), i * 40) for i in range(1, 4)]
        self.enemy_directions = [random.choice([-1, 1]) for _ in self.enemies]  # Direction de chaque ennemi (-1 pour gauche, 1 pour droite)

        # Décalage vertical pour simuler le défilement
        self.scroll_offset = 0

        # Réinitialiser le flag de "Game Over"
        self.game_over = False

    def update(self):
        if self.game_over:
            # Réinitialiser le jeu si Game Over et la touche R est pressée
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        self.update_player()
        self.update_enemies()
        self.check_collisions()

        # Si le joueur dépasse la moitié de l'écran en hauteur, décaler le décor
        if self.player_y < WINDOW_HEIGHT // 2:
            self.scroll_offset += 1
            self.player_y += 1  # Ajuster légèrement le joueur pour simuler l'ascension continue
            self.score += 1  # Augmenter le score lorsqu'on avance dans le jeu

            # Déplacer les plateformes et ennemis vers le bas
            self.platforms = [(x, y + 1) for x, y in self.platforms]
            self.enemies = [(ex, ey + 1) for ex, ey in self.enemies]

            # Supprimer les plateformes en bas et en ajouter en haut
            self.platforms = [
                (x, y) for x, y in self.platforms if y < WINDOW_HEIGHT
            ]
            if len(self.platforms) < 5:
                new_platform_y = min(y for _, y in self.platforms) - 30
                new_platform_x = random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH)
                self.platforms.append((new_platform_x, new_platform_y))

            # Supprimer les ennemis en bas et en ajouter en haut
            self.enemies = [
                (ex, ey) for ex, ey in self.enemies if ey < WINDOW_HEIGHT
            ]
            while len(self.enemies) < 3:
                new_enemy_y = min(ey for _, ey in self.enemies) - 40 if self.enemies else 0
                new_enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
                self.enemies.append((new_enemy_x, new_enemy_y))
                self.enemy_directions.append(random.choice([-1, 1]))

    def update_player(self):
        # Déplacement horizontal
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2
        
        if pyxel.btn(pyxel.KEY_DOWN) and not self.on_ground :
            self.player_y -= 0.3

        # Appliquer la gravité uniquement si le joueur n'est pas au sol
        if not self.on_ground:
            self.player_dy += GRAVITY
            # Limiter la vitesse de chute maximale
            if self.player_dy > MAX_FALL_SPEED:
                self.player_dy = MAX_FALL_SPEED
            self.player_y += self.player_dy

        # Saut : Si le joueur est sur le sol, il peut sauter
        if self.on_ground and pyxel.btnp(pyxel.KEY_SPACE):
            self.player_dy = JUMP_STRENGTH
            self.on_ground = False

        # Garder le joueur dans les limites de l'écran
        self.player_x = max(0, min(WINDOW_WIDTH - PLAYER_WIDTH, self.player_x))
        self.player_y = min(WINDOW_HEIGHT - PLAYER_HEIGHT, self.player_y)

        # Si le joueur tombe en bas de l'écran
        if self.player_y >= WINDOW_HEIGHT - PLAYER_HEIGHT :
            self.lives -= 1
            if self.lives > 0:
                self.reset_game(keep_score=True)  # Garde le score et enlève une vie
            else:
                self.game_over = True

    def update_enemies(self):
        for i, (ex, ey) in enumerate(self.enemies):
            # Déplacer chaque ennemi dans sa direction
            direction = self.enemy_directions[i]
            ex += direction

            # Changer de direction si l'ennemi atteint les bords de l'écran
            if ex <= 0:
                ex = 0
                self.enemy_directions[i] = 1  # Tourner vers la droite
            elif ex >= WINDOW_WIDTH - ENEMY_WIDTH:
                ex = WINDOW_WIDTH - ENEMY_WIDTH
                self.enemy_directions[i] = -1  # Tourner vers la gauche

            self.enemies[i] = (ex, ey)

    def check_collisions(self):
        # Réinitialiser `self.on_ground` pour vérifier s'il est en contact avec une plateforme
        self.on_ground = False
        for (px, py) in self.platforms:
            # Vérifier la collision entre le joueur et la plateforme
            if (
                self.player_x + PLAYER_WIDTH > px
                and self.player_x < px + PLATFORM_WIDTH
                and self.player_y + PLAYER_HEIGHT <= py  # Le joueur est juste au-dessus de la plateforme
                and self.player_y + PLAYER_HEIGHT + self.player_dy >= py  # Le joueur tombe vers la plateforme
                and self.player_dy >= 0  # La vitesse verticale est dirigée vers le bas ou nulle
            ):
                # Ajuster la position du joueur juste au-dessus de la plateforme
                self.player_y = py - PLAYER_HEIGHT
                self.player_dy = 0  # Arrêter la gravité (vitesse verticale)
                self.on_ground = True
                break  # Sortir de la boucle après avoir détecté une collision

        # Vérification de collision avec les ennemis
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
                    self.reset_game(keep_score=True)
                else:
                    self.game_over = True

    def draw(self):
        pyxel.cls(0)
        # Dessiner le joueur
        pyxel.rect(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, 9)

        # Dessiner les plateformes
        for (px, py) in self.platforms:
            pyxel.rect(px, py, PLATFORM_WIDTH, PLATFORM_HEIGHT, 11)

        # Dessiner les ennemis (oiseaux)
        for (ex, ey) in self.enemies:
            pyxel.rect(ex, ey, ENEMY_WIDTH, ENEMY_HEIGHT, 8)

        # Afficher le score, les vies et instructions
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Vies: {self.lives}", 7)
        

        # Afficher Game Over si le joueur n'a plus de vies
        if self.game_over:
            pyxel.text(40, 60, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(20, 70, "Appuyez sur R pour rejouer", pyxel.COLOR_WHITE)

# Lancer le jeu
ClimberGame()