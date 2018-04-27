import time,pygame,os,math
from pygame import mixer,display
s=time.time()
mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
mixer.init()
mixer.music.load(os.path.join("unused","swoosh.mp3"))
mixer.music.set_volume(1.0)
mixer.music.play()
window=display.set_mode((1920,1080),pygame.FULLSCREEN)
while time.time()-s<13.4:
 window.fill([math.sin((time.time()-s)*0.5)*126+127,math.sin((time.time()-s)*0.75+5)*126+127,math.sin(time.time()-s)*126+127])
 display.flip()
pygame.quit()