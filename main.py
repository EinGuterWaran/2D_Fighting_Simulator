import random
import pygame


class Map:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = [[0 for a in range(y)] for b in range(x)]

    def update(self, x, y, val):
        self.map[x][y] = val


class Fighter:
    def __init__(self, name, life, strength, speed, crit, id):
        self.name = name
        self.life = life
        self.strength = strength
        self.speed = speed
        self.crit = crit
        self.id = id
        self.temp = life
        self.x = None
        self.y = None

    def delete(self, map):
        map.update(self.x, self.y, 0)

    def put(self, map):
        map.update(self.x, self.y, self.id)

    def heal(self):
        self.temp = self.life

    def attack(self, fighters, x, y, tp, stats):
        for fighter in fighters:
            if fighter.x == x and fighter.y == y:
                victim = fighter
        min_power = round(self.strength * 0.7, 0)
        max_power = round(self.strength * 1.3, 0)
        critFactor = 1
        isCrit = random.randint(1, 101)
        if isCrit <= round(self.crit / 10, 2):
            critFactor = 3
        how_hard = round(
            critFactor * random.randint(min_power, max_power) / 10, 2)
        victim.temp -= how_hard
        victim.temp = round(victim.temp, 2)
        stats[self.id]["damage"] += how_hard
        stats[self.id]["damage"] = round(stats[self.id]["damage"], 2)
        stats[self.id]["hits"] += 1
        if critFactor == 3:
            the_text1 = "KABOOM! A critical hit. "
            stats[self.id]["crit"] += 1

        else:
            the_text1 = "BAM! "
        the_text2 = ""
        if victim.temp <= 0:
            the_text2 = "and KILLS "
            stats[self.id]["kills"] += 1
        the_text = the_text1 + self.name + " attacks " + the_text2 + victim.name + ". He loses " + str(
            how_hard) + " life."
        print(the_text)
        tp.append(the_text)

    def move(self, map, fighters, tp, stats):
        moves = 1
        for a in range(0, 2):
            x = random.randint(1, 1001)
            if self.speed * 3 >= x:
                moves += 1
        for b in range(0, moves):
            where = random.randint(1, 4)
            if where == 1:
                self.up(map, fighters, tp, stats)
            elif where == 2:
                self.down(map, fighters, tp, stats)
            elif where == 3:
                self.right(map, fighters, tp, stats)
            elif where == 4:
                self.left(map, fighters, tp, stats)

    def left(self, map, fighters, tp, stats):
        if not self.x - 1 < 0 and map.map[self.x - 1][self.y] == 0:
            self.delete(map)
            self.x -= 1
            self.put(map)
        elif not self.x - 1 < 0 and not map.map[self.x - 1][self.y] == 0:
            self.attack(fighters, self.x - 1, self.y, tp, stats)

    def right(self, map, fighters, tp, stats):
        if not self.x + 1 == map.x and map.map[self.x + 1][self.y] == 0:
            self.delete(map)
            self.x += 1
            self.put(map)
        elif not self.x + 1 == map.x and not map.map[self.x + 1][self.y] == 0:
            self.attack(fighters, self.x + 1, self.y, tp, stats)

    def up(self, map, fighters, tp, stats):
        if not self.y - 1 < 0 and map.map[self.x][self.y - 1] == 0:
            self.delete(map)
            self.y -= 1
            self.put(map)
        elif not self.y - 1 < 0 and not map.map[self.x][self.y - 1] == 0:
            self.attack(fighters, self.x, self.y - 1, tp, stats)

    def down(self, map, fighters, tp, stats):
        if not self.y + 1 == map.y and map.map[self.x][self.y + 1] == 0:
            self.delete(map)
            self.y += 1
            self.put(map)
        elif not self.y + 1 == map.y and not map.map[self.x][self.y + 1] == 0:
            self.attack(fighters, self.x, self.y + 1, tp, stats)


def simulate_game(map, fighters):
    amount_fig = len(fighters)
    death_prints = []
    fighters2 = fighters.copy()
    textPipe = []
    textPipeLen = 0
    stats = {}
    for fighter in fighters:
        stats[fighter.id] = {}
        stats[fighter.id]["kills"] = 0
        stats[fighter.id]["damage"] = 0
        stats[fighter.id]["hits"] = 0
        stats[fighter.id]["crit"] = 0
        stats[fighter.id]["name"] = fighter.name
        while True:
            x = random.randint(0, map.x - 1)
            y = random.randint(0, map.y - 1)
            if map.map[x][y] == 0:
                break
        map.map[x][y] = fighter.id
        fighter.x = x
        fighter.y = y
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
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
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # --- Game logic should go here
        for fighter in fighters:
            if fighter.temp <= 0:
                deadText = fighter.name + " is dead."
                textPipe.append(deadText)
                death_prints.append([
                    deadText,
                    [map.x * 40 + 10, 40 * (amount_fig - len(fighters))]
                ])
                print(deadText)
                fighter.delete(map)
                fighters.remove(fighter)
        for d_p in death_prints:
            font = pygame.font.SysFont('Calibri', 15, True, False)
            text = font.render(d_p[0], True, RED)
            screen.blit(text, d_p[1])

        for fighter in fighters:
            fighter.move(map, fighters, textPipe, stats)
        # --- Drawing code should go here
        for x in range(0, map.x):
            for y in range(0, map.y):
                font = pygame.font.SysFont('Calibri', 25, True, False)
                if map.map[x][y] != 0:
                    text = font.render(str(map.map[x][y]), True, BLACK)
                    screen.blit(text, [x * 40, y * 40])
        fighterCounter = 0
        for fighter in fighters2:
            font = pygame.font.SysFont('Calibri', 15, True, False)
            text = font.render(
                fighter.name + ", " + str(fighter.temp) + "/" +
                str(fighter.life), True, BLUE)
            screen.blit(
                text,
                [map.x * 40 + 10, 40 * (amount_fig) + 40 * fighterCounter])
            fighterCounter += 1

        if len(fighters) == 1:
            done = True
            font = pygame.font.SysFont('Calibri', 15, True, False)
            the_text = fighters[0].name + " won!!"
            text = font.render(the_text, True, GREEN)
            print(the_text)
            textPipe.append(the_text)
            for x in stats:
                x = stats[x]
                the_text2 = x["name"] + ", KILLS: " + str(
                    x["kills"]) + ", DAMAGE: " + str(x["damage"])+", HITS: "+str(x["hits"])+", CRITIAL HITS: "+str(x["crit"])
                print(the_text2)
                textPipe.append(the_text2)

            fighters[0].delete(map)
            fighters.remove(fighters[0])
            screen.blit(text, [map.x * 40 + 10, 40 * (amount_fig - 1)])
        # mode = [textPipeLen, textPipeLen]
        mode = [15, len(textPipe) - 15]
        if len(textPipe) > mode[0] and mode[0] > 0:
            for x in range(0, mode[1]):
                textPipe.pop(0)
        textCounter = 0
        textPipeLen = len(textPipe)
        for text in textPipe:
            font = pygame.font.SysFont('Calibri', 10, True, False)
            text2 = font.render(text, True, BLACK)
            screen.blit(text2, [40, map.y * 40 + 40 + textCounter * 15])
            textCounter += 1
        pygame.display.update()
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        # --- Go ahead and update the screen with what we've drawn.
        # --- Limit to x frames per second
        clock.tick(10)


def example():
    map = Map(10, 5)
    otto = Fighter("Otto", 33, 100, 1, 93, "O")
    hans = Fighter("Hans", 34, 50, 350, 94, "H")
    peter = Fighter("Peter", 35, 95, 95, 95, "P")
    walter = Fighter("Walter", 36, 96, 96, 96, "W")
    gerd = Fighter("Gerd", 37, 97, 97, 97, "G")
    janu = Fighter("Janu", 200, 200, 350,1000, "Janu")
    simulate_game(map, [otto, hans, peter, walter, janu])


def main():
    while True:
      mode = input("Enter e if you want to see an example game. If you want to set up your own game enter o! ")
      if mode=="e" or mode=="o":
        break
      print("That's not e or o!")
    if mode=="e":
      example()
    elif mode=="o":
      while True:
        mapx = input("Map width (10 or higher): ")
        if str(mapx).isnumeric() and int(mapx) >=10:
          break
        print("Please enter a number (10 or higher)!")
      while True:
        mapy = input("Map height (5 or higher): ")
        if str(mapy).isnumeric() and int(mapy) >=5:
          break
        print("Please enter a number (5 or higher)!")
      mapx = int(mapx)
      mapy = int(mapy)
      map = Map(mapx,mapy)
      player_index = 0
      players=[]
      while True:
        while True:
          name = input("Name of player #"+str(player_index+1)+": ")
          if type(name) is str:
            break
        while True:
          life = input("Life of "+name+": ")
          if life.isnumeric():
            break
        while True:
          strength = input("Strength of "+name+": ")
          if strength.isnumeric():
            break
        while True:
          speed = input("Speed of "+name+": ")
          if speed.isnumeric():
            break
        while True:
          crit = input("Critical hit of "+name+": ")
          if crit.isnumeric():
            break
        while True:
          id = input("ID of "+name+": ")
          if type(id) is str:
            break
        players.append([name,int(life),int(strength),int(speed),int(crit),id])
        while True:
          end = input("Enter y if you want to add another player. If not, enter n! ")
          if end=="y" or end=="n":
            break
          print("That's not y or n!")
        if end == "n":
          break
        player_index += 1
      players2=[]
      for player in players:
          players2.append(Fighter(player[0], player[1], player[2], player[3],player[4], player[5]))
      simulate_game(map, players2)

if __name__ == "__main__":
    # example()
    main()
