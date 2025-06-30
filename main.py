from os import listdir
from os.path import join, isfile
import pygame as pg
from sys import exit

pg.init()

FPS: int = 60
CLOCK = pg.time.Clock()
WIDTH, HEIGHT = 1000, 780
WIN = pg.display.set_mode((WIDTH, HEIGHT))
PLAYER_VEL = 5

pg.display.set_caption('PLATFORMER')

def flip(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction  = False):
    path = join("assets", dir1, dir2)
    images  = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image)).convert_alpha()
        sprites = []
        
        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pg.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace('.png', '') +  '_right'] = sprites
            all_sprites[image.replace('.png', '') +  '_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites

    return all_sprites

def draw_background(image_name):
    image = pg.image.load(join('assets', 'Background', image_name))
    _, _, w, h = image.get_rect()
    tile_map = [
        (i * w, j * h) 
        for i in range(WIDTH // w + 1) 
        for j in range(HEIGHT // h + 1)
    ]

    for tile in tile_map: WIN.blit(image, tile)

def draw(player, objects):
    draw_background('Purple.png')
    player.draw()

    for obj in objects:
        obj.draw()

    pg.display.update()

def handle_move(player):
    keys = pg.key.get_pressed()

    player.x_vel = 0
    if keys[pg.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pg.K_RIGHT]:
        player.move_right(PLAYER_VEL)

def load_block(size):
    path = join('assets', 'Terrain', 'Terrain.png')
    image = pg.image.load(path).convert_alpha()
    surface = pg.Surface((size, size), pg.SRCALPHA, 32)
    rect = pg.Rect(96, 128, size, size)
    surface.blit(image, (0, 0), rect)
    return pg.transform.scale2x(surface)

class Player(pg.sprite.Sprite):
    COLOR = (225, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets('MainCharacters', 'PinkMan', 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left': 
            self.direction = 'left'
            self.animation_count = 0
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right': 
            self.direction = 'right'
            self.animation_count = 0

    def loop(self, fps):
        # self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.x_vel != 0:
            sprite_sheet = 'run'

        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites =  self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index] 
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)
    
    def draw(self):
        WIN.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name = None):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.width = w
        self.height = h
        self.name = name
    
    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = load_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pg.mask.from_surface(self.image)

def main() -> None: 
    player = Player(100, 100, 50, 50) 
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        player.loop(FPS)
        handle_move(player)
        draw(player, floor)

        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()