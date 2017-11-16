import pygame, math, time
from pygame.locals import *

pygame.init()

scrW = 500

window = pygame.display.set_mode([scrW, scrW])

window.fill([255, 255, 255])

boop = pygame.Surface([10, 10]).convert()
boop.fill([0, 0, 0])
window.blit(boop, [scrW // 2 - 5, scrW // 2 - 5])

gameExit = False

angle = 0

while not gameExit:
    mousePos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
    window.fill([255, 255, 255])
    pygame.draw.aaline(window, [255, 0, 0], [(scrW / 2), (scrW / 2)], mousePos, 2)
    window.blit(pygame.font.Font(None, 36).render(str(angle), 1, [10, 10, 10]), [0, 0])
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            gameExit = True

    if mousePos[0] - (scrW / 2) > 0:
        if mousePos[1] - (scrW / 2) > 0:
            angle = ((180 / math.pi) * math.atan((mousePos[1] - (scrW / 2))/(mousePos[0] - (scrW / 2))))
        else:
            angle = ((180 / math.pi) * math.atan((mousePos[1] - (scrW / 2))/(mousePos[0] - (scrW / 2))))
    elif mousePos[0] - (scrW / 2) < 0:
        angle = ((180 / math.pi) * math.atan((mousePos[1] - (scrW / 2))/(mousePos[0] - (scrW / 2))))
    else:
        mousePos[0] += 1
        if mousePos[0] - (scrW / 2) > 0:
            angle = ((180 / math.pi) * math.atan((mousePos[1] - (scrW / 2))/(mousePos[0] - (scrW / 2))))
        else:
            angle = (-1 * (180 / math.pi) * math.atan((mousePos[1] - (scrW / 2))/(mousePos[0] - (scrW / 2))))

pygame.quit()