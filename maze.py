from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Treasure(GameSprite):
    pass


class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height, rgb_color=(0, 0, 0)):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill(rgb_color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


init()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))
clock = time.Clock()
FPS = 60

mixer.music.load('jungles.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

text_font = font.Font(None, 80)
win_text = text_font.render('YOU WIN!', True, (255, 215, 0))
lose_text = text_font.render('YOU LOSE!', True, (180, 0, 0))

player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
treasure = Treasure('treasure.png', win_width - 120, win_height - 80, 0)

wall_color = (154, 205, 50)
walls = sprite.Group(
    Wall(100, 100, 10, 400, wall_color),
    Wall(110, 250, 60, 10, wall_color),
    Wall(250, 0, 10, 380, wall_color),
    Wall(420, 100, 10, 400, wall_color),
)

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        treasure.reset()
        for w in walls:
            w.draw_wall()

        if sprite.collide_rect(player, monster) or sprite.spritecollide(player, walls, False):
            finish = True
            window.blit(lose_text, lose_text.get_rect(center=(win_width // 2, win_height // 2)))
            kick.play()

        elif sprite.collide_rect(player, treasure):
            finish = True
            window.blit(win_text, win_text.get_rect(center=(win_width // 2, win_height // 2)))
            money.play()

    display.update()
    clock.tick(FPS)