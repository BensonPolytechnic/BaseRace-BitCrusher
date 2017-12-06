import pygame, time, random, threading, multiprocessing
from pygame.locals import *

class blitThread(threading.Thread):
   def __init__(self, startPoint, dims):
      threading.Thread.__init__(self)
      self.startPoint = startPoint
      self.currentPixel = pygame.Surface([1, 1]).convert()
      self.dims = dims
   def run(self):
      for x in range(self.dims[0]):
          for y in range(self.dims[1]):
              self.currentPixel.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
              window.blit(self.currentPixel, [self.startPoint[0] + x, self.startPoint[1] + y])
              

global window

window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

fuckyou = multiprocessing.cpu_count() - 1

freds = []

for butts in range(fuckyou):
    freds.append(blitThread([butts * 100, butts * 100], [100, 100]))

for ffff in freds:
    ffff.start()

while threading.activeCount() > 1:
    pass

pygame.display.flip()

startTime = time.clock()

while time.clock() < startTime + 5:
    pass

pygame.quit()
