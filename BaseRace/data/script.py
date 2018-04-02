import time,pygame,os,math
from pygame.locals import*
startTime=time.time()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("Sounds","swoosh.mp3"))
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()
window=pygame.display.set_mode((1920,1080),pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
while time.time()-startTime<13.4:
 window.fill([int(math.sin((time.time()-startTime)*0.5)*126)+127,int(math.sin((time.time()-startTime)*0.75+5)*126)+127,int(math.sin(time.time()-startTime)*126)+127])
 pygame.display.flip()
pygame.quit()