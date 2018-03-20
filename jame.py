#coding=utf-8
import random, pygame, sys
from pygame.locals import *

class Drawable(object):
  """Anything, that can be drawed"""
  def draw(self):
    pass

class Neurono(Drawable):
  """Damn Neuron"""
  def __init__(self, tav=None,ny = 0):
    self.y = ny
    self.cy = ny
    self.tav = tav
    self.x = tav.x
    self.r = gs['neuron_r']
    self.cr = gs['neuron_r']
    self.mode = random.randrange(2)
    self.mouse = 0
    self.en = []
    self.el = []
    self.block = 0
    
  def draw(self):
    for l in self.el:
      l.draw()
    pygame.draw.circle(neuron_layer,gs['color'][2][self.block],self.getCpos(), int(self.cr*1.2))
    pygame.draw.circle(neuron_layer, gs['color'][self.mouse][self.mode],self.getCpos(), self.cr)
    
  def update(self, dt):
    if self.cr > self.r:
      self.cr = int(self.cr/gs['dscale'])
    if self.cr < self.r:
      self.cr = int(gs['dscale']*self.cr)
    self.x = self.tav.x
    self.cx = self.tav.cx
    if self.cy > self.y:
      self.cy -= gs['dspeed']
   # else:
    if self.cy < self.y:
      self.cy += gs['dspeed']
    if not self.block:
      mx = gs['mouse'][0]
      my = gs['mouse'][1]
      if (mx > self.x - self.r*2) and (mx < self.x + self.r*2) and (my > self.y - self.r*2) and (my < self.y + self.r*2):
        self.mouse = 1
        if gs['l_mouse']:
          gs['l_mouse'] = False
          self.mode = (self.mode + 1) %2
      else:
        self.mouse = 0
#    print ("out links: %d in links:%d" % (len(self.en),len(self.el)))
   
  def spamSignal(self, mode):
    for l in self.el:
      l.signal = Signalo(l,mode)
      
  def getSum(self):
    ret = 0
    for n in self.en:
      if n.signal != None:
        ret+=n.signal.mode
    return ret
    
  def change(self):
    if self.mode > 0:
      self.mode = 0
    else:
      self.mode = 1

  def getFor(self):
    ret = []
    for l in self.el:
      ret.append(l.al)
    return ret
      
  def postLink(self,t):
    for n in t.neuronoj:
      if n not in self.getFor():
        self.el.append(Ligo(self,n))
        n.en.append(self.el[-1])        

  def preLink(self,t):
    for n in t.neuronoj:
      if self not in n.getFor():
        n.el.append(Ligo(n,self))
        self.en.append(n.el[-1])        

      
  def setPos(self, xy):
    self.tav.x = xy[0]
    self.y = xy[1]
  
  def getCpos(self):
    return (self.tav.cx, self.cy)

  def getPos(self):
    return (self.tav.x, self.y)

class Respondo(Drawable):
  """Correct answer for variant"""
  def __init__(self,mode):
    self.mode = mode
    self.y = gs['r_line']
    self.r = gs['r_rad']    

  def draw(self, x):
    pygame.draw.circle(signal_layer,gs['color'][1][self.mode],(int(x),self.y), int(self.r))

class Ligo(Drawable):
  """ Link between neurons"""
  def __init__(self, de, al):
    self.de = de
    self.al = al
    self.signal = None
    self.wid = gs['link_w']
    
  def draw(self):
    pygame.draw.line(link_layer, (100,100,100), self.de.getCpos(), self.al.getCpos(),self.wid)
    if self.signal!= None:
      self.signal.draw()

class Point(object):
  """ Simple point in space"""
  
  def __init__(self,nx,ny):
    self.x = nx
    self.y = ny
  
  def getPos(self):
    return (self.x, self.y)

class Signalo(Drawable):
  """Signal, cxu ne?"""
  
  def __init__(self, ligo, mode):
#    print ("Creating signal from node (%d %d) to (%d %d" % (ligo.de.tav.x, ligo.de.y, ligo.al.tav.x, ligo.al.y))
    self.mode = mode
    self.ligo = ligo
    self.x = 0
    self.r = gs['signal_r']
    
  def draw(self):
    self.r = gs['signal_r']
    de = self.ligo.de
    al = self.ligo.al
    pygame.draw.circle(signal_layer,gs['color'][1][self.mode],(de.tav.sig_x, int(de.cy + (al.cy - de.cy)*de.tav.vojo)), int(self.r))

class Tavolo(Drawable):
  """Yes"""
  def __init__(self,x):
    self.x = x
    self.cx = x
    self.sig_x = x
    self.neuronoj = []
    self.busy = False
    self.vojo = 0.0
    self.next = None
    self.prev = None
    self.expand = False
    self.resp = None
    self.addNeuron()
    
  def addNeuron(self):
#    if self.busy:
#      self.expand = True
#      return
    if self.prev != None:
      if self.busy or self.prev.busy:
        #print (str(self.busy) +' '+str(self.prev.busy))
        self.expand = True
        return
    ny = int(gs['field_hei']/2+gs['field_y'])
    if len(self.neuronoj)>0:
      ny = self.neuronoj[-1].y
    self.neuronoj.append(Neurono(self,ny))
    if self.next != None:
      self.neuronoj[-1].postLink(self.next) 
    if self.prev != None:
      self.neuronoj[-1].preLink(self.prev) 
    for i in range(len(self.neuronoj)):
      self.neuronoj[i].y = int(gs['field_y'] + (i+1) * gs['field_hei'] / (len(self.neuronoj)+1))
    if len(self.neuronoj) > gs['max_neuronoj']:
      gs['max_neuronoj'] = len(self.neuronoj)
    self.expand = False
  
  def spamSignal(self, rand=False):
    if self.next != None:
      if self.next.expand:
        return False
    self.busy = True
    self.vojo = 0.0
    
    if rand:
      self.resp = Respondo(random.randrange(2))
      for n in self.neuronoj:
        sig = random.randrange(2)
        n.spamSignal(sig)
        n.mode = sig
        
    else:
      for n in self.neuronoj:
        self.resp = self.prev.resp
#        self.prev.resp = None
        if (n.mode==1 and n.getSum()>=len(n.en)/2) or (n.mode==0 and n.getSum()<=len(n.en)/2):
          n.spamSignal(1)
        else:
          n.spamSignal(0)
    return True
          
  def forLink(self):
    for n in self.neuronoj:
      n.el = []
    if self.next != None:
      for n in self.next.neuronoj:
        n.en = []

  def update(self, dt):                 
    if self.cx > self.x:
      self.cx -= gs['dspeed']
    if self.cx < self.x:
      self.cx += gs['dspeed']
    if self.expand:
      self.addNeuron()
    if self.busy and self.vojo < 1.0:
      self.vojo += dt*gs['speed'] / 10000
    inter = gs['field_wid']/len(reto.tavoloj)
    if self.next != None:
      inter = self.next.cx - self.cx
    self.sig_x = int(self.cx + inter*self.vojo)
    if self.busy and self.vojo >= 1.0:
      if self.vojo > 1.0:
        self.vojo = 1.0
      if self.next != None:
 #       if self.next.busy == False:
 #         if self.next.next!= None:
 #           if not self.next.next.expand:
 #             self.next.spamSignal()
          if self.next.next == None:
            n = self.next.neuronoj[0]
            if n.getSum()>=len(n.en)/2:
              n.mode = 1
            else:
              n.mode = 0
            gs['end_signal'] = True
            gs['end_signal_pars'] = {'ans':n.mode,'correct':self.resp.mode}
          if self.next.spamSignal():
            self.busy = False
          #self.vojo = 0.0
      else:
#FINISH YOUR FUCKING STORY!
       # n = self.neuronoj[0]
     #   if n.getSum()>=len(n.en)/2:
      #    n.mode = 1
       # else:
       #   n.mode = 0
        self.vojo = 0.0
        self.busy = False
    for n in self.neuronoj:
      n.update(dt)
      n.r = gs['neuron_r']
      for l in n.el:
        l.wid = gs['link_w']
  
  def draw(self):
    for n in self.neuronoj:
      n.draw() 
    if self.resp != None and self.busy:
      self.resp.draw(self.sig_x)

class Reto(Drawable):
  """Yes"""
  def __init__(self):
    self.tavoloj = []
    self.tavoloj.append(Tavolo(int(gs['field_x'] + gs['field_wid'] / 2)))
    self.addTavolo() #output layer
    self.expand = False
    self.tavoloj[0].cx = gs['field_x']
    self.tavoloj[1].cx = gs['field_x']+gs['field_wid']
    
  def linkReton(self):
    for i in range(len(self.tavoloj)-1):
      for n in self.tavoloj[i].neuronoj:
        n.postLink(self.tavoloj[i+1]) 
  
  def forLink(self, t1):
    pass
  
  def draw(self):
    neuron_layer.fill((0,0,0,0))
    link_layer.fill((0,0,0,0))
    signal_layer.fill((0,0,0,0))
    for t in self.tavoloj:
      t.draw()
    screen.blit(link_layer,(0,0))
    screen.blit(signal_layer,(0,0))
    screen.blit(neuron_layer,(0,0))
    pts = tetra.render(gs['text']['points'][gs['lang']] + str(gs['points']), True, (255, 255, 255))
    divacc = '-'
    if gs['signals']!=0:
      divacc = str(int(gs['correct']*100/gs['signals']))
    if gs['provoj']<=0:
      lose = bigtetra.render(gs['text']['lose'][gs['lang']],True, (255, 0, 0))
      lose_pts = bigtetra.render(gs['text']['lose_pts'][gs['lang']]+str(gs['points']),True, (255, 0, 0))
      screen.blit(lose, ((gs['field_wid']+gs['field_x']*2 - lose.get_width())/2,gs['field_hei']/2))
      screen.blit(lose_pts, ((gs['field_wid']+gs['field_x']*2 - lose_pts.get_width())/2,gs['field_hei']/2+100))
    acc = tetra.render(gs['text']['acc'][gs['lang']] + divacc +'%', True, (255, 255, 255))
    spd = tetra.render(gs['text']['speed'][gs['lang']] + gs['text']['speed_desc'][int(gs['speed']/5)-1][gs['lang']], True, (255, 255, 255))
    cor = tetra.render(gs['text']['cor'][gs['lang']],True,(0,gs['cor_blend'],0))
    malcor = tetra.render(gs['text']['necor'][gs['lang']],True,(gs['malcor_blend'],0,0))
    screen.blit(pts,(10,50)) 
    screen.blit(acc,(210,50)) 
    screen.blit(spd,(410,50)) 
    if gs['malcor_blend']<=0:
      screen.blit(cor,(gs['field_x']+gs['field_wid'] - cor.get_width()/2,gs['field_hei']/2)) 
    if gs['cor_blend']<=0:
      screen.blit(malcor,(gs['field_wid']+gs['field_x'] - malcor.get_width()/2,gs['field_hei']/2)) 


  def update(self, dt):
    
    gs['cor_blend'] -= gs['speed'] / 2
    if gs['cor_blend'] < 0:
      gs['cor_blend'] = 0
    gs['malcor_blend'] -= gs['speed']/2
    if gs['malcor_blend'] < 0:
      gs['malcor_blend'] = 0

    if (gs['provoj']<=0):
      gs['neuron_r'] = 0
      gs['signal_r'] = 0
      gs['link_w'] = 0
      for t in self.tavoloj:
        t.update(dt)
      return

    spam = 0
    if gs['field_wid'] / len (self.tavoloj) > gs['field_hei'] / (gs['max_neuronoj']):
      spam = gs['field_hei'] / gs ['max_neuronoj']
    else:
      spam = gs['field_wid'] / len (self.tavoloj)
  
    if gs['end_signal']:
      gs['end_signal'] = False
      gs['signals']+=1
      if gs['signals']>=gs['expand_time']:
        expand()
        gs['expand_int']+=gs['expand_mod']
        gs['expand_time']+=gs['expand_int']
      if gs['end_signal_pars']['ans'] == gs['end_signal_pars']['correct']:
        gs['correct'] +=1
        gs['points'] = int(gs['points'] + 1)
        gs['cor_blend'] = 255
        gs['provoj'] += 1.0 - gs['dif']
      else:
        gs['malcor_blend'] = 255
        gs['provoj'] -= 1

    gs['neuron_r'] = int(spam / 6)
    gs['signal_r'] = int(spam / 12)
    gs['link_w'] = int(spam / 16)
    if self.expand == False:
      if self.tavoloj[0].busy == False and not self.tavoloj[1].expand:
        self.tavoloj[0].spamSignal(rand=True)
    else:
      self.addTavolo()
    for t in self.tavoloj:
      t.update(dt)
 
  def addTavolo(self):
#   for t in self.tavoloj:
#      if t.busy:
#        self.expand = True
#        return
    if len(self.tavoloj) > 1:
      if self.tavoloj[0].busy or self.tavoloj[1].busy:
        self.expand = True
        return
    self.tavoloj.insert(1,Tavolo(self.tavoloj[0].x))
    if len(self.tavoloj)>1:
      self.tavoloj[0].forLink()
      self.tavoloj[0].next = self.tavoloj[1]
      self.tavoloj[1].prev = self.tavoloj[0]
      if len(self.tavoloj) > 2:
        self.tavoloj[1].next = self.tavoloj[2]
        self.tavoloj[2].prev = self.tavoloj[1]
    for i in range(len(self.tavoloj)):
      self.tavoloj[i].x = int(gs['field_x'] + i * gs['field_wid'] / (len(self.tavoloj)-1))    
    self.linkReton() 
    self.expand = False

  def getUnua(self):
    """returns input layer"""
    return self.tavoloj[0]

  def getLasta(self):
    """returns output layer"""
    return self.tavoloj[len(self.tavoloj)-1]

class Menu(object):
  def __init__(self):
    t = gs['text']
    cent = gs['field_x']+ gs['field_wid']/2
    self.entries = []
    self.entries.append(Continue(t['cont'],cent,200))
    self.entries.append(Start(t['start'],cent,250))
    self.entries.append(Change(t['lang'],cent,300))
    self.entries.append(Exit(t['exit'],cent,350))

  def update(self):
    if gs['state']=='menu':
      for e in self.entries:
        e.update()
 
  def draw(self):
    title = bigtetra.render('KOVRITA',True, (255, 255, 255))
    mes = tetra.render(gs['text']['mes'][gs['lang']],True, (255, 255, 255))
    screen.blit(title,(gs['field_wid']/2+gs['field_x'] - title.get_width()/2,50))
    screen.blit(mes,(gs['field_wid']/2+gs['field_x'] - mes.get_width()/2,550))
    for e in range(len(self.entries)):
      if not (e==0 and not gs['pause']): 
        screen.blit(self.entries[e].surf,(self.entries[e].x-self.entries[e].surf.get_width()/2,self.entries[e].y))

class Entry(object):

  def __init__(self, text, x, y, active = True):
    self.form = "%s"
    self.pars = text
    self.x = x 
    self.y = y
    self.chcap()
    self.mouse = 0
    self.surf = menu_font.render(self.out,True,gs['butt_color'][self.mouse])

  def update(self):
    mx = gs['mouse'][0]
    my = gs['mouse'][1]
    top = self.y - self.surf.get_height()/2
    bot = self.y + self.surf.get_height()/2
    left = self.x - self.surf.get_width()/2
    right = self.x + self.surf.get_width()/2
    if (mx > left) and (mx < right) and (my > top) and (my < bot):
      self.mouse = 1
      if gs['l_mouse']:
        gs['l_mouse'] = False
        self.click()
    else:
      self.mouse = 0
    if self.lang != gs['lang']:
      self.chcap()
    self.surf = menu_font.render(self.out,True,gs['butt_color'][self.mouse])

  def chcap(self):
    self.lang = gs['lang']
    self.out = self.form % (self.pars[self.lang])
  
  def click(self):
    pass

class Continue(Entry):
  def click(self):
    gs['state'] = 'game'

class Start(Entry):
  def click(self):
    gs['state'] = 'game'
    newgame()

class Change(Entry):
  def click(self):
    if gs['lang'] == 'eo':
      gs['lang'] = 'en'
    else:
      gs['lang'] = 'eo'

class Exit(Entry):
  def click(self):
    if gs['state']=='menu':
      exit()
    else:
      gs['state'] = 'menu'

def expand():
  if len(reto.tavoloj)==2 or (gs['max_neuronoj'] +1 > len(reto.tavoloj)):
    reto.addTavolo()
  elif len(reto.tavoloj[1].neuronoj)==1:
    reto.tavoloj[1].addNeuron()
  elif len(reto.tavoloj)>=3 and (random.randrange(2)==0 or len(reto.tavoloj) + 1 > gs['max_neuronoj']):
    pool = []
    for t in range(len(reto.tavoloj)-1)[1:]:
      if (len(reto.tavoloj[t].neuronoj) <= len(reto.tavoloj[t].next.neuronoj) or t == len(reto.tavoloj)-2) and (len(reto.tavoloj[t].neuronoj) <= len(reto.tavoloj[t].prev.neuronoj) or t == 1):
        pool.append(reto.tavoloj[t])
    pool[random.randrange(len(pool))].addNeuron()
  else:
    reto.addTavolo()

def newgame():
  gs['signal_r'] = 10
  gs['r_rad'] = 20
  gs['neuron_r'] = 20
  gs['link_w'] = 5
  gs['max_neuronoj'] = 1
  gs['end_signal'] = False
  gs['end_signal_pars'] = []
  gs['expand_mod'] = 5
  gs['expand_int'] = gs['expand_mod']
  gs['expand_time'] = gs['expand_mod']
  gs['speed'] = 15.0
  gs['dspeed'] = 10
  gs['dscale'] = 1.05 
  gs['result'] = None
  gs['signals'] = 0
  gs['correct'] = 0
  gs['dif'] = 0.8
  gs['points'] = 0
  gs['provoj'] = gs['dif'] * 10
  gs['respoj'] = []
  gs['cor_blend'] = 0
  gs['malcor_blend'] = 0
  
  global reto
  reto = Reto()
  reto.getUnua().neuronoj[0].block = 1
  reto.getUnua().neuronoj[0].mode = 2
  reto.getLasta().neuronoj[0].block = 1
  reto.getLasta().neuronoj[0].mode = 2
  for i in range(1):
    expand()
  reto.linkReton()
  reto.draw()



pygame.init()

FPS = 60
global fpsClock
global screen
global gs
global menu

text = {}
text['lose'] = {'en':'You Lose!','ru':'Вы проиграли!','eo':'Vi fiaskis!'}
text['lose_pts'] = {'en':'Your Score: ','ru':'Ваш счёт: ','eo':'Via sukceso: '}
text['points'] = {'en':'Points: ','ru':'Очки: ','eo':'Punktoj: '}
text['acc'] = {'en':'Accuracy: ','ru':'Точность: ','eo':'Ghusteco: '}
text['cor'] = {'en':'Correct!','ru':'Правильно!','eo':'Korekte!'}
text['necor'] = {'en':'Uncorrect!','ru':'Неправильно!','eo':'Nekorekte!'}
text['start'] = {'en':'Start Game','ru':'Начать игру','eo':'Komenci ludon'}
text['cont'] = {'en':'Continue Game','ru':'Продолжить игру','eo':'Dauhrigi ludo'}
text['exit'] = {'en':'Quit Game','ru':'Выход из игры','eo':'Eliri'}
text['lang'] = {'en':'Language: English','ru':'Язык:  Русский','eo':'Lingvo: Esperanto'}
text['lang'] = {'en':'Language: English','ru':'Язык:  Русский','eo':'Lingvo: Esperanto'}
text['speed'] = {'en':'Speed: ','ru':'Скорость: ','eo':'Rapideco: '}
text['speed_desc'] = [{'en':'Very Slow','ru':'Лениво','eo':'Malrapidege'},
                      {'en':'Slow','ru':'Медленно','eo':'Malrapide'},
                      {'en':'Normal','ru':'Нормально','eo':'Normale'},
                      {'en':'Fast','ru':'Быстро','eo':'Rapide'},
                      {'en':'Ultra','ru':'Молниеносно','eo':'Rapidege'}]
text['mes'] = {'en':'This game was created for Igronic Game Crunch Jam by Artemo Arbaletos, May 2017','ru':'Эта игра была сделана для Игроничного Джема Артемием Арбалетосом, Май 2017.','eo':'Tiu chi ludo estis farita speciale por Igronika Ghemo de Ludokrako per Artemo Arbaletos, Majo 2017.'}

gs = {}
gs['text'] = text
gs['lang'] = 'eo'
gs['s_wid'] = 800
gs['s_hei'] = 600
gs['field_wid'] = 600
gs['field_hei'] = 400
gs['field_x'] = 100
gs['field_y'] = 100
gs['butt_color'] = [(255,255,255),(150,150,255)]
gs['color'] = [[(0,0,200),(200,0,0),(0,0,0)],[(100,100,250),(250,100,100),(0,0,0)],[(0,0,0),(100,100,100)]]
gs['l_mouse'] = False
gs['r_line'] = gs['field_y'] + gs['field_hei']
tetra = pygame.font.Font("Tetra.ttf",16)
bigtetra = pygame.font.Font("Tetra.ttf",64)
menu_font = pygame.font.Font("Tetra.ttf",40)
fpsClock = pygame.time.Clock()
menu = Menu()
screen = pygame.display.set_mode((800,600),FULLSCREEN)
link_layer = pygame.surface.Surface((800, 600),flags=SRCALPHA, depth=32)
neuron_layer = pygame.surface.Surface((800, 600), flags=SRCALPHA, depth=32)
signal_layer = pygame.surface.Surface((800, 600), flags=SRCALPHA, depth=32)
gs['state'] = 'menu'
gs['pause'] = False
pygame.display.set_caption("Kovrita")

while True: # the main game loop
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        if gs['state'] == 'menu':
          exit()
        else:
          gs['pause'] = True
          gs['state'] = 'menu'
      if event.key == K_RETURN:
         if gs['provoj']<=0:
           newgame()
#        expand()
      if event.key == K_LEFT:
        if gs['speed']>5:
         gs['speed']-=5
      if event.key == K_RIGHT:
        if gs['speed']<25:
          gs['speed']+=5
    mouse = pygame.mouse.get_pressed()
    if mouse[0] and not gs['l_mouse']:
      gs['l_mouse'] = True
    if not mouse[0] and gs['l_mouse']:
      gs['l_mouse'] = False
    gs['mouse'] = pygame.mouse.get_pos()
 # expand()
  screen.fill((0,0,0))
  if gs['state'] == 'game':
    reto.update(1000/FPS)
    reto.draw()
  else:
    menu.update()
    menu.draw()
  pygame.display.update()
  fpsClock.tick(FPS)
