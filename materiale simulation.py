import pygame,sys,random,colorsys

#starter pygame
pygame.init()

#definere variabler
window_width = 800
window_height = 600
node_size = 6
fps = 120
grey = (10, 10, 10)
light_grey = (55, 55, 55)
clock = pygame.time.Clock()

#opretter vindue
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Materiale Simulation")


#laver gitter klassen som skal holde styr på alle nodes i spillet
class Grid:
    def __init__(self,width,height,node_size):
        self.rows = height // node_size
        self.cols = width // node_size
        self.node_size = node_size
        self.nodes = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self,window):
        for row in range(self.rows):
            for col in range(self.cols):
                particle = self.nodes[row][col]
                if particle is not None:
                    color = particle.color
                    pygame.draw.rect(window, color, (col * self.node_size, row * self.node_size, self.node_size, self.node_size))
    
    def add_particle(self, row, col, particle_type):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.nodes[row][col] = particle_type()

    def remove_particle(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.nodes[row][col] = None
    def is_node_empty(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.nodes[row][col] is None:
                return True
        return False
    
    def set_node(self, row, col, particle):
        if not(0 <= row < self.rows and 0 <= col < self.cols):
            return
        self.nodes[row][col] = particle
   
    def get_node(self, row, col):
        if (0 <= row < self.rows and 0 <= col < self.cols):
            return self.nodes[row][col]
        return None
      


class sand:
    def __init__(self):
        self.color = self.random_color()

    def random_color(self):
        hue = random.uniform(0.1,0.12)
        saturation = random.uniform(0.5,0.7)
        value = random.uniform(0.6,0.8)
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return int(r * 255), int(g * 255), int(b * 255)
    def update(self, grid, col, row):
        if grid.is_node_empty(row + 1, col):
            return row + 1, col
        else:
            offsets =[-1,1]
            random.shuffle(offsets)
            for offset in offsets:
                new_col = col + offset
                if grid.is_node_empty(row + 1, new_col):
                    return row + 1, new_col
        return row, col
        

class Simulation:
    def __init__(self,width,height,node_size):
        self.grid = Grid(width, height, node_size)

    def draw(self,window):
        self.grid.draw(window)
    def add_particle(self, row, col):
        self.grid.add_particle(row, col, sand)
    def remove_particle(self, row, col):
        self.grid.remove_particle(row, col)
    def update(self):
        for row in range(self.grid.rows-2, -1, -1):
            for col in range(self.grid.cols):
                particle = self.grid.get_node(row, col)
                if particle is not None:
                    new_pos = particle.update(self.grid, col, row)
                    if new_pos != (row, col):
                        self.grid.set_node(new_pos[0], new_pos[1], particle)
                        self.grid.remove_particle(row, col)

simulation = Simulation(window_width, window_height, node_size)

simulation.add_particle(0,0)
simulation.add_particle(1,1)


simulation.remove_particle(0,0)


#main loop
while True:
    #event handling
    #loops som tjekker for events, i dette tilfælde om brugeren har klikket på krydset for at lukke vinduet, og hvis det er tilfældet, så lukker programmet ned
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        pos = pygame.mouse.get_pos()
        row = pos[1] // node_size
        col = pos[0] // node_size
        simulation.add_particle(row, col)

    #draw stuff
    window.fill(grey)
    simulation.draw(window)

    # opdaterer displayet og sætter fps
    simulation.update()
    pygame.display.flip()
    clock.tick(fps)
