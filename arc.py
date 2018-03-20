class Drawable(object):
  """Anything, that can be drawed"""
  def draw(self):
    pass

class Neurono(Drawable):
  """Damn Neuron"""
  def __init__(self):
    self.x = 0
    self.y = 0
    self.r = gs['neuron_r']
    self.mode = 0
    self.mouse = 0
    self.en = []
    self.el = []
    
  def draw(self):
    pygame.draw.circle(screen, color[self.mouse][self.mode],self.getPos(), self.r)
    
  def update(self):
    pass
   
  def change(self):
    if self.mode > 0:
      self.mode = 0
    else:
      self.mode = 1
      
  def postLink(self,t):
    for n in t:
      if n not in self.el:
        self.el.append(Ligo(self,n))
        n.en.append(self.el[-1])        
      
  def setPos(self, xy):
    self.x = xy[0]
    self.y = xy[1]

  def getPos(self):
    return (self.x, self.y)

class Ligo(Drawable):
  """ Link between neurons"""
  def __init__(self, de, al):
    self.de = de
    self.al = al
    self.wid = gs['link_w']
    
  def draw(self):
    pygame.draw.line(screen, (0,0,0), self.el.Getpos(), self.al.Getpos(),self.wid)

class Signalo(Drawable):
  """Signal, cxu ne?"""
  
  def __init__(self, ligo, mode):
    self.mode = mode
    self.ligo = ligo
    self.vojo = 0.0
    self.r = gs['signal_r']
    
  def draw(self):
    pygame.draw.circle(screen,color[0][self.mode],(self.ligo.el.x + (self.ligo.al.x-self.ligo.el.x)*self.vojo, self.ligo.el.y+ (self.ligo.al.y-self.ligo.el.y)*self.vojo), self.r)
    

class Tavolo(Drawable):
  """Yes"""
  def __init__(self):
    self.x = 0
    self.neuronoj = []
    
  def addNeuron(self):
    self.neuronoj.append(Neurono())
    for i in range(len(self.tavoloj)):
      self.tavoloj[i].x = gs['field_y'] + (i+1) * gs['field_hei'] / (len(self.tavoloj)+1)

  def draw(self):
    for n in self.neuronoj:
      n.draw()  

class Reto(Drawable):
  """Yes"""
  def __init__(self):
    self.tavoloj = []
    self.tavoloj.append(Tavolo()) #input layer
    self.tavoloj.append(Tavolo()) #output layer
    
  def linkReton(self):
    for i in range(len(self.tavoloj-1)):
      for n in self.tavoloj[i]:
        n.postLink(self.tavoloj[i+1])   
  def forLink(self, t1):
    pass
  
  def draw(self):
    for t in self.tavoloj:
      t.draw()
   
  def update(self, dt):
     for t in self.tavoloj:
       t.update(dt)

  def addTavolo(self):
    self.tavoloj.append(Tavolo())
    if len(self.tavoloj)==1:
      self.tavoloj[0].x = gs['field_x'] + gs['field_wid'] / 2
    else: 
      for i in range(len(self.tavoloj)):
        self.tavoloj[i].x = gs['field_x'] + i * gs['field_wid'] / (len(self.tavoloj))
  
  def getUnua(self):
    """returns input layer"""
    return self.tavoloj[0]

  def getLasta(self):
    """returns output layer"""
    return self.tavoloj[len(self.tavoloj)-1]

