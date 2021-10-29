import random
import pygame

class map:
  def __init__(self, x, y): 
        self.x = x 
        self.y = y 
        self.map = [[0 for a in range(y)] for b in range(x)] 

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
  def heal(self):
        self.temp = self.life
  def left(self, map):
    if not self.x - 1 < 0:
      self.x -= 1
  def right(self, map):
     if not self.x + 1 == map.x:
      self.x += 1
  def up(self, map):
    if not self.y - 1 < 0:
      self.y -= 1
  def down(self, map):
     if not self.y + 1 == map.y:
      self.y += 1

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
  GREEN    = (   0, 255,   0)
  RED      = ( 255,   0,   0)
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
        where = random.randint(1,4)
        if where == 1:
          fighter.up(map)
        elif where == 2:
          fighter.down(map)
        elif where == 3:
          fighter.right(map)
        elif where == 4:
          fighter.left(map)
      for x in range(0,len(map.map)):
        for y in range(0,len(map.map[x])):
          if map.map[x][y] != 0:
            who = map.map[x][y]
            for fighter in fighters:
              if fighter.id == who:
                if (fighter.x != x) or (fighter.y != y):
                  map.map[x][y] = 0
                  map.map[fighter.x][fighter.y] = fighter.id
      # --- Drawing code should go here
      for x in range(0,len(map.map)):
        for y in range(0,len(map.map[x])):
          font = pygame.font.SysFont('Calibri', 25, True, False)
          text = font.render(str(map.map[x][y]),True,BLACK)
          screen.blit(text, [x*40, y*40])
      pygame.display.update()
      
      # First, clear the screen to white. Don't put other drawing commands
      # above this, or they will be erased with this command.
      screen.fill(WHITE)
      # --- Go ahead and update the screen with what we've drawn.
      # pygame.display.flip()
  
      # --- Limit to 60 frames per second
      clock.tick(5)
  
map = map(3,5)
otto = Fighter("Otto", 93, 93, 93, 1)
hans = Fighter("Hans", 94, 94, 94, 2)
simulate_game(map,[otto,hans])
print(map.map)
