import pygame
from random import randrange

width = 800  # ширина игрового окна
heigh = 600 # высота игрового окна
size = 20
fps = 10 # частота кадров в секунду
score = 0

pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((width, heigh))
pygame.display.set_caption("Rikoshet")
clock = pygame.time.Clock()
x, y = 300, heigh-size
player = [(x, y)]
dx, dy = 0, 0
xb, yb = 400, heigh-size*2
ball = [(xb, yb)]
dxb, dyb = -1, -1
target = randrange(size*2, width-size*3, size), randrange(size*2, heigh/2, size)
directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
font_score = pygame.font.SysFont('Consolas', 20, bold=True)
font_end = pygame.font.SysFont('Arial', 75, bold=True)

while True:
    screen.fill(pygame.Color('black'))
    [(pygame.draw.rect(screen, pygame.Color('white'), (i, j, size*10, size))) for i, j in player]
    [(pygame.draw.rect(screen, pygame.Color('yellow'), (i, j, size, size))) for i, j in ball]
    pygame.draw.rect(screen, pygame.Color('red'), (*target, size*3, size*3))
    x += dx * size
    y += dy * size
    player.append((x, y))
    player = player[-1:]
    xb += dxb * size
    yb += dyb * size
    ball.append((xb, yb))
    ball = ball[-1:]
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('green'))
    screen.blit(render_score, (5, 5))

    pygame.display.flip()
    clock.tick(fps)
    #ball moving
    if xb == 0 and directions.get('Up') and directions.get('Left'):
        dxb, dyb = 1, -1
        directions = {'Left': False, 'Right': True, 'Up': True, 'Down': False}
    if xb == 0 and directions.get('Down') and directions.get('Left'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': False, 'Down': True}
    if yb == 0 and directions.get('Up') and directions.get('Right'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': False, 'Down': True}
    if yb == 0 and directions.get('Up') and directions.get('Left'):
        dxb, dyb = -1, 1
        directions = {'Left': True, 'Right': False, 'Up': False, 'Down': True}
    if xb == width-size and directions.get('Up') and directions.get('Right'):
        dxb, dyb = -1, -1
        directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
    if xb == width-size and directions.get('Down') and directions.get('Right'):
        dxb, dyb = -1, 1
        directions = {'Left': True, 'Right': False, 'Up': False, 'Down': True}
    #ball touch player
    if x-10 <= xb <= x+size*10 and yb == heigh-size*2 and directions.get('Left'):
        dxb, dyb = -1, -1
        directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
    if x-10 <= xb <= x+size*10 and yb == heigh-size*2 and directions.get('Right'):
        dxb, dyb = 1, -1
        directions = {'Left': False, 'Right': True, 'Up': True, 'Down': False}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    #touching target
    #зліва
    if xb == target[0]-size and target[1] <= yb <= target[1]+size*2 and directions.get('Up'):
        dxb, dyb = -1, -1
        directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    if xb == target[0]-size and target[1] <= yb <= target[1]+size*2 and directions.get('Down'):
        dxb, dyb = -1, 1
        directions = {'Left': True, 'Right': False, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #знизу
    if yb == target[1]+size*3 and target[0] <= xb <= target[0]+size*2 and directions.get('Right'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    if yb == target[1] + size * 3 and target[0] <= xb <= target[0] + size * 2 and directions.get('Left'):
        dxb, dyb = -1, 1
        directions = {'Left': True, 'Right': False, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #справа
    if xb == target[0]+size*3 and target[1] <= yb <= target[1]+size*2 and directions.get('Up'):
        dxb, dyb = 1, -1
        directions = {'Left': False, 'Right': True, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    if xb == target[0] + size * 3 and target[1] <= yb <= target[1] + size * 2 and directions.get('Down'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #зверху
    if yb == target[1]-size and target[0] <= xb <= target[0]+size*2 and directions.get('Right'):
        dxb, dyb = 1, -1
        directions = {'Left': False, 'Right': True, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    if yb == target[1] - size and target[0] <= xb <= target[0] + size * 2 and directions.get('Left'):
        dxb, dyb = -1, -1
        directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #зверху зліва
    if yb == target[1]-size and xb == target[0]-size and directions.get('Down') and directions.get('Right'):
        dxb, dyb = -1, -1
        directions = {'Left': True, 'Right': False, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #знизу справа
    if yb == target[1]+size*3 and xb == target[0]+size*3 and directions.get('Up') and directions.get('Left'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #знизу зліва
    if yb == target[1]+size*3 and xb == target[0]-size and directions.get('Up') and directions.get('Right'):
        dxb, dyb = -1, 1
        directions = {'Left': True, 'Right': False, 'Up': False, 'Down': True}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #зверху справа
    if xb == target[0]+size*3 and yb == target[1]-size and directions.get('Down') and directions.get('Left'):
        dxb, dyb = 1, 1
        directions = {'Left': False, 'Right': True, 'Up': True, 'Down': False}
        target = randrange(0, width - size * 2, size), randrange(size, heigh / 2, size)
        fps += 1
        score += 1
    #user controlling
    if x == 0 or x == width-size*10:
        dx, dy = 0, 0
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        dx, dy = -1, 0
    if key[pygame.K_d]:
        dx, dy = 1, 0
    #game ending
    if yb == heigh:
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            screen.blit(render_end, (int(width/2-200), int(heigh/2-50)))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
