from sys import exit
import pygame as pg

pg.init()

FPS: int = 60
CLOCK = pg.time.Clock()
WIDTH, HEIGHT = 1000, 780
WIN = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption('PLATFORMER')

def draw():
    pass

def main() -> None:
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        pg.display.update()
        CLOCK.tick(FPS)

if __name__ == '__main__':
    main()