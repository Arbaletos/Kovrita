class Menu(object)
  def __init__(self):
    text = gs['text']
    self.entries = []
    self.entries.append(ContinueGame(
    self.entries.append(StartGame(
    self.entries.append(ChSpeed(
    self.entries.append(ChDifficult(
    self.entries.append(ChLanguage(
    self.entries.append(ChScreen(
    self.entries.append(ShowHelp(
    self.entries.append(ShowStory(
    self.entries.append(ShowCredits(
    self.entries.append(Exit(
    
    self.entries.append(ChDif(gs['diff']),x,y)
    self.entries.append(StartGame(gs['']),x,y)


  def update(self):
    if gs['state']=='menu':
      for e in self.entries:
        e.update
    else
  
  def draw(self):
    for e in range(len(self.entries)):
      if not (e==0 and reto==None):
        screen.blit(e.surf,e.x,y)
    
class Changer(Entry):
  """ Entries of type 'Putin: President', t.e. witg changed val"""
  def __init__(self, form, pars, par):
    self.form = form
    self.pars = pars
    self.par = par
    
  def chcap(self):
    self.lang = gs['lang']
    self.out = self.form % (self.pars[0][self.lang],self.pars[1][self.par][self.lang])

class Entry(object):

  def __init__(self, text):    
    self.form = "%s"
    self.pars = text
    self.chcap()
    
  def update(self):
    """Changes color if mouseon, changes lingvo, clicking"""
    if mouse on:
      color = light
      if click:
        self.click()
        self.chcap()
    else:
      color = dark
    if gs['lang']!=self.lang:
      self.chcap()
    self.sur = pygane.render.e.t.c()   
      
  def chcap(self):
    self.lang = gs['lang']
    self.out = self.form % (self.pars[self.lang])
   
  def click(self):
    pass
    
class InfoEntry(Entry):
  def __init__(self, text, info):
    super.__init__
    self.info = info
    
  def click(self):
    gs['state'] = 'text'
    gs['info'] = self.info[self.lang]
    
class ContinueGame(Entry):
  def click(self):
    gs['state']='menu'
    
    
class StartGame(Entry):
  def click(self):
    """ New Game """
    gs['state'] = 'game'
    reto = new reto e.t.c.

class Exit(Entry):
  def click(self):
    if gs['state']=='menu':
      sys.exit()
    else:
      gs['state'] = 'menu' 
  

  

text = {}
text['diff'] = ({},[])
text['start'] = {'en':'Start Game','ru':'Начать игру','eo':'Komenci ludon'}
text['exit'] = {}
	
gs['text']='text'
gs['state']='menu' #menu, text or game
gs['lang']='eo'

reto = None
  :
  if jey,== escape:
    if state == menu:
      sys.exit()
    else:
      state == menu
  if gs['state'] = 'game':
    reto.update
    reto.draw e.t.c.
  else:
    menu.update
    menu.drae
