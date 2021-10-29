import random
import pygame

class Map:
  def __init__(self, x, y): 
        self.x = x 
        self.y = y 
        self.map = [[0 for a in range(y)] for b in range(x)]
  def update(self,x,y,val):
    self.map[x][y] = val

class Fighter:
  def __init__(self, name, strength, life, crit,id): 
        self.name = name 
        self.strength = strength 
        self.life = life
        self.crit = crit
        self.temp = life
        self.id = id
        self.x = None
        self.y = None
  def delete(self,map):
      map.update(self.x,self.y,0)
  def update(self,map):
      map.update(self.x,self.y,self.id)
  def heal(self):
      self.temp = self.life
  def attack(self, fighters,x,y):
      for fighter in fighters:
        if fighter.x==x and fighter.y==y:
          victim = fighter
      minPower = round(self.strength*0.7,0)
      maxPower = round(self.strength*1.3,0)
      victim.temp -= round(random.randint(minPower, maxPower)/10,2)
      victim.temp = round(victim.temp,2)
      print("KABOOM!")

  def left(self, map, fighters):
    if not self.x - 1 < 0 and map.map[self.x-1][self.y] == 0:
      self.delete(map)
      self.x -= 1
      self.update(map)
    elif not self.x - 1 < 0 and not map.map[self.x-1][self.y] == 0:
      self.attack(fighters,self.x-1,self.y)

  def right(self, map, fighters):
    if not self.x + 1 == map.x and map.map[self.x+1][self.y] == 0:
      self.delete(map)
      self.x += 1
      self.update(map)
    elif not self.x + 1 == map.x and not map.map[self.x+1][self.y] == 0:
      self.attack(fighters,self.x+1,self.y)

  def up(self, map, fighters):
    if not self.y - 1 < 0 and map.map[self.x][self.y-1] == 0:
      self.delete(map)
      self.y -= 1
      self.update(map)
    elif not self.y - 1 < 0 and not map.map[self.x][self.y-1] == 0:
      self.attack(fighters,self.x,self.y-1)

  def down(self, map, fighters):
    if not self.y + 1 == map.y and map.map[self.x][self.y+1] == 0:
      self.delete(map)
      self.y += 1
      self.update(map)
    elif not self.y + 1 == map.y and not map.map[self.x][self.y+1] == 0:
      self.attack(fighters,self.x,self.y+1)

def simulate_game(map,fighters):
  for fighter in fighters:
    while True:
      x = random.randint(0,map.x-1)
      y = random.randint(0,map.y-1)
      if map.map[x][y] == 0:
        break
    map.map[x][y] = fighter.id
    fighter.x = x
    fighter.y = y
  # Define some colors
  BLACK    = (   0,   0,   0)
  WHITE    = ( 255, 255, 255)
  # GREEN    = (   0, 255,   0)
  # RED      = ( 255,   0,   0)
  BLUE     = (   0,   0, 255)
  pygame.init()
  size = (700, 500)
  screen = pygame.display.set_mode(size)  
  pygame.display.set_caption("2Dfight")
  # Loop until the user clicks the close button.
  done = False
  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()
  # -------- Main Program Loop -----------
  while not done:
      # --- Main event loop
      for event in pygame.event.get(): # User did something
          if event.type == pygame.QUIT: # If user clicked close
              done = True # Flag that we are done so we exit this loop

      # --- Game logic should go here
      for fighter in fighters:
        if fighter.temp <= 0:
          print(fighter.name+" is dead.")
          done = True
        else:
          where = random.randint(1,4)
          if where == 1:
            fighter.up(map, fighters)
          elif where == 2:
            fighter.down(map, fighters)
          elif where == 3:
            fighter.right(map, fighters)
          elif where == 4:
            fighter.left(map, fighters)
      # --- Drawing code should go here
      for x in range(0,map.x):
        for y in range(0,map.y):
          font = pygame.font.SysFont('Calibri', 25, True, False)
          if map.map[x][y] != 0:
            text = font.render(str(map.map[x][y]),True,BLACK)
            screen.blit(text, [x*40, y*40])
      fighterCounter = 0  
      for fighter in fighters:
        font = pygame.font.SysFont('Calibri', 15, True, False)
        text = font.render(fighter.name+", "+str(fighter.temp)+"/"+str(fighter.life), True, BLUE)
        screen.blit(text, [map.x*40+10, map.y*40+20*fighterCounter])
        fighterCounter+=1
      pygame.display.update()
      # First, clear the screen to white. Don't put other drawing commands
      # above this, or they will be erased with this command.
      screen.fill(WHITE)
      # --- Go ahead and update the screen with what we've drawn.  
      # --- Limit to 60 frames per second
      clock.tick(5)

def main():
  map = Map(5,2)
  otto = Fighter("Otto", 93, 93, 93, "O")
  hans = Fighter("Hans", 94, 94, 94, "H")
  simulate_game(map,[otto,hans])
  print(map.map)

if __name__ == "__main__":
  main()