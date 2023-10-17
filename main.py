import pygame
import random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Game:
    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        self.round = 1
        self.score = 0
        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        self.font = pygame.font.Font("Facon.ttf", 45)

    def update(self):
        self.game_over()
        self.breach()
        self.draw()
        self.check_collisions()
        self.new_round()

    def move_alien(self):
        for alien in self.alien_group:
            alien.rect.x += alien.velocity

    def draw(self):
        pygame.draw.line(screen, WHITE, (0, 64), (WINDOW_WIDTH, 64), 3)
        pygame.draw.line(screen, WHITE, (0, 600), (WINDOW_WIDTH, 600), 3)
        self.round_text = self.font.render(f"round: {self.round}", True, WHITE)
        self.round_rect = self.round_text.get_rect()
        self.round_rect.topleft = (10, 20)

        self.score_text = self.font.render(f"score: {self.score}", True, WHITE)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.topleft = (500, 20)

        self.lives_text = self.font.render(f"lives: {self.player.lives}", True, WHITE)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.topleft = (900, 20)

        screen.blit(self.round_text, self.round_rect)
        screen.blit(self.lives_text, self.lives_rect)
        screen.blit(self.score_text, self.score_rect)

    def check_collisions(self):
        for alien in self.alien_group:
            if pygame.sprite.spritecollide(alien, self.player_bullet_group, True):
                alien.kill()
                self.score += self.round*100
        if pygame.sprite.spritecollide(self.player, self.alien_bullet_group, True):
            self.player.lives -= 1

    def pause_game(self):
        paused = True
        while paused:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        paused = False

            round_text = self.font.render(f"space invader round {self.round}", True, WHITE)
            enter_text = self.font.render("press 'enter' to begin", True, WHITE)

            round_rect = round_text.get_rect()
            round_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60)

            enter_rect = enter_text.get_rect()
            enter_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

            screen.blit(round_text, round_rect)
            screen.blit(enter_text, enter_rect)
            pygame.display.update()

    def breach(self):
        for alien in self.alien_group.sprites():
            if alien.rect.y > 550:
                self.player.lives += -1
                pause = True
                while pause:
                    screen.fill(BLACK)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                for alien2 in self.alien_group.sprites():
                                    alien2.rect.y -= 200
                                    pause = False

                    breach_text = self.font.render("you have been breached!", True, WHITE)
                    breach_rect = breach_text.get_rect()
                    breach_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50)

                    resume_text = self.font.render("press 'enter' to continue", True, WHITE)
                    resume_rect = resume_text.get_rect()
                    resume_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

                    screen.blit(breach_text, breach_rect)
                    screen.blit(resume_text, resume_rect)

                    pygame.display.update()

    def game_over(self):
        if self.player.lives == 0:
            is_paused = True
            while is_paused:
                screen.fill(BLACK)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        global running
                        is_paused = False
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.player.lives = 5
                            self.score = 0
                            self.round = 1
                            self.alien_group.empty()
                            for i in range(0, 11):
                                for j in range(1, 6):
                                    a_alien = Alien(i * 64, j * 64, my_alien_group)
                                    self.alien_group.add(a_alien)
                                    is_paused = False


                final_score_text = self.font.render(f"final score: {self.score}", True, WHITE)
                final_score_rect = final_score_text.get_rect()
                final_score_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60)

                play_again_text = self.font.render("press 'enter' to play again", True, WHITE)
                play_again_rect = play_again_text.get_rect()
                play_again_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

                screen.blit(final_score_text, final_score_rect)
                screen.blit(play_again_text, play_again_rect)

                pygame.display.update()

    def new_round(self):
        if not self.alien_group:
            self.round += 1
            self.pause_game()
            for i in range(0, 11):
                for j in range(1, 6):
                    a_alien = Alien(i * 64, j * 64, my_alien_group)
                    a_alien.velocity += self.round - 1
                    self.alien_group.add(a_alien)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (600, 690)
        self.lives = 5
        self.velocity = 7

    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.left -= self.velocity
        if keys[pygame.K_RIGHT]:
            if self.rect.right < WINDOW_WIDTH:
                self.rect.right += self.velocity

    def shoot(self):
        PlayerBullet(my_player, my_bullet_group)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_group):
        super(Alien, self).__init__()
        self.velocity = 2
        self.alien_group = alien_group
        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.shift_down()
        self.shoot()

    def shift_down(self):
        for alien in self.alien_group.sprites():
            if alien.rect.right >= WINDOW_WIDTH:
                for alien in self.alien_group:
                    alien.rect.y += 10
                    alien.rect.x -= 10
                    alien.velocity *= -1
            if alien.rect.left <= 0:
                for alien in self.alien_group:
                    alien.rect.y += 10
                    alien.rect.x += 10
                    alien.velocity *= -1

    def shoot(self):
        num = random.randint(0, 850)
        if num == 6:
            AlienBullet(self, my_alien_bullet_group)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, player, bullet_group):
        super(PlayerBullet, self).__init__()
        self.velocity = 10
        self.player = player
        self.bullet_group = bullet_group
        self.image = pygame.image.load("green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.player.rect.x + 30, self.player.rect.y)
        self.bullet_group.add(self)

    def update(self):
        self.bullet()

    def bullet(self):
        self.rect.y -= self.velocity
        if self.rect.y < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, alien, bullet_group):
        super(AlienBullet, self).__init__()
        self.velocity = 10
        self.alien = alien
        self.bullet_group = bullet_group
        self.image = pygame.image.load("red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.alien.rect.x + 30, self.alien.rect.y)
        self.bullet_group.add(self)

    def update(self):
        self.bullet()

    def bullet(self):
        self.rect.y += self.velocity
        if self.rect.y > WINDOW_HEIGHT:
            self.kill()

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

my_bullet_group = pygame.sprite.Group()

my_alien_bullet_group = pygame.sprite.Group()

my_alien_group = pygame.sprite.Group()
for i in range(0, 11):
    for j in range(1, 6):
        a_alien = Alien(i*64, j*64, my_alien_group)
        my_alien_group.add(a_alien)

my_game = Game(my_player, my_alien_group, my_bullet_group, my_alien_bullet_group)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(my_bullet_group.sprites()) < 2:
                    my_player.shoot()
    screen.fill(BLACK)

    my_game.update()
    my_game.move_alien()

    my_player_group.update()
    my_player_group.draw(screen)

    my_bullet_group.update()
    my_bullet_group.draw(screen)

    my_alien_group.update()
    my_alien_group.draw(screen)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()