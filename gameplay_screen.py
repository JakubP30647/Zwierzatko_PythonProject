import random
import sys

import utils
from settings import *
from utils import FUN
from widgets import *

def gameplay_screen(screen):

    font = pygame.font.Font('assets/milk.ttf', int(HEIGHT * 0.037))

    loveImg = pygame.image.load('assets/love.png')
    loveList = []

    back_button = Button(WIDTH * 0.8, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "BACK", font)
    petButton = Button(WIDTH * 0.20, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "PET", font)
    foodButton = Button(WIDTH * 0.40, HEIGHT * 0.9, WIDTH * 0.15, HEIGHT * 0.052, "Feed", font)

    funBar = Bar(WIDTH * 0.005, HEIGHT * 0.02, WIDTH * 0.15, HEIGHT * 0.05, 100)
    funBar.ratio = utils.FUN
    funBar.color1 = GRAY
    funBar.color2 = GREEN

    foodBar = Bar(WIDTH * 0.005, HEIGHT * 0.10, WIDTH * 0.15, HEIGHT * 0.05, 100)
    foodBar.ratio = utils.FOOD
    foodBar.color1 = GRAY
    foodBar.color2 = BLUE

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    last_drop_time_fun = 0
    last_drop_time_food = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(background, (0, 0))
        clock.tick(60)
        currentTime = pygame.time.get_ticks()

        for x in loveList:
            if len(loveList) > 0:
                if abs(x.x - WIDTH / 2) <= WIDTH * 0.1 and abs(x.y - HEIGHT / 2) <= HEIGHT * 0.1:
                    loveList.remove(x)
                    break

                if x.x < WIDTH / 2:
                    x.x += WIDTH * 0.00156  # 3px = 3 / 1920
                else:
                    x.x -= WIDTH * 0.00156

                if x.y < HEIGHT / 2:
                    x.y += HEIGHT * 0.00278  # 3px = 3 / 1080
                else:
                    x.y -= HEIGHT * 0.00278

        for x in loveList:
            x.draw(screen)

        if currentTime - last_drop_time_fun > 1000:
            funBar.ratio -= 1
            last_drop_time_fun = currentTime

        if currentTime - last_drop_time_food > 750:
            foodBar.ratio -= 1
            last_drop_time_food = currentTime

        funBar.draw(screen)
        foodBar.draw(screen)

        petButton.draw(screen)
        foodButton.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    return "main_menu"
                if petButton.is_clicked(event.pos):
                    riseRatio(funBar)
                    loveList.append(
                        LoveEntity(
                            random.randint(0, int(WIDTH * 0.26)),  # 500 / 1920 = 0.26
                            random.randint(0, int(HEIGHT * 0.46)),  # 500 / 1080 = 0.46
                            loveImg
                        )
                    )
                if foodButton.is_clicked(event.pos):
                    riseRatio(foodBar)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu"
                if event.key == pygame.K_SPACE:
                    riseRatio(funBar)
                    loveList.append(
                        LoveEntity(
                            random.randint(0, int(WIDTH * 0.26)),
                            random.randint(0, int(HEIGHT * 0.46)),
                            loveImg
                        )
                    )
                if event.key == pygame.K_e:
                    riseRatio(foodBar)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def riseRatio(bar):
    if bar.ratio < 90:
        bar.ratio += 10
    elif bar.ratio >= 0:
        bar.ratio += 100 - bar.ratio


class LoveEntity:

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
