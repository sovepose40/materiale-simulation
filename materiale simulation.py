import pygame,sys,random,colorsys

#starter pygame
pygame.init()
pygame.mouse.set_visible(False)
#definere variabler
window_width = 800
window_height = 600
node_size = 6
fps = 144
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
        if 0 <= row < self.rows and 0 <= col < self.cols and self. is_node_empty(row, col):
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
    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.remove_particle(row, col)
      


class sand:
    def __init__(self):
        self.color = random_color((0.1, 0.12), (0.5, 0.7), (0.7, 0.9))

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
class rock:
    def __init__(self):
        self.color = random_color((0, 0.1), (0.1, 0.3), (0.3, 0.5))

def random_color(hue_range,saturation_range,value_range):
    hue = random.uniform(*hue_range)
    saturation = random.uniform(*saturation_range)
    value = random.uniform(*value_range)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)



class Simulation:
    def __init__(self,width,height,node_size):
        self.grid = Grid(width, height, node_size)
        self.node_size = node_size
        self.mode="sand"
        self.brush_size=3

    def update(self):
        for row in range(self.grid.rows-2, -1, -1):
            if row % 2 == 0:    
                col_range = range(self.grid.cols)
            else:
                col_range = reversed(range(self.grid.cols))
            for col in col_range:
                particle = self.grid.get_node(row, col)
                if isinstance(particle, sand):
                    new_pos = particle.update(self.grid, col, row)
                    if new_pos != (row, col):
                        self.grid.set_node(new_pos[0], new_pos[1], particle)
                        self.grid.remove_particle(row, col)

    def draw(self,window):
        self.grid.draw(window)
        self.draw_brush(window)

    def add_particle(self, row, col):
        if self.mode=="sand":
            if random.random() < 0.15:
                self.grid.add_particle(row, col, sand)
        elif self.mode=="rock":
           self.grid.add_particle(row, col, rock)   
    
    def remove_particle(self, row, col):
        self.grid.remove_particle(row, col)

    def restart(self):
        self.grid.clear()
    def handle_controls(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                self.handle_key(event)
        self.handle_mouse()

    def handle_key(self,event):
        if event.key == pygame.K_SPACE:
                self.restart()
        elif event.key == pygame.K_s:
                print("sand mode")
                self.mode="sand"
        elif event.key == pygame.K_r:
                print("rock mode")
                self.mode="rock"
        elif event.key == pygame.K_e:
                print("eraser mode")
                self.mode="eraser"

    def handle_mouse(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            pos = pygame.mouse.get_pos()
            row = pos[1] // self.node_size
            col = pos[0] // self.node_size

            self.apply_brush(row, col)


    def apply_brush(self, row, col):
        for r in range(self.brush_size):
            for c in range(self.brush_size):
                current_row = row + r
                current_col = col + c
                if self.mode == "eraser":
                    self.remove_particle(current_row, current_col)
                else:
                    self.add_particle(current_row, current_col)
    def draw_brush(self,window):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // self.node_size
        col = mouse_pos[0] // self.node_size

        brush_visual_size = self.brush_size * self.node_size
        color=(255,255,255)

        if self.mode == "eraser":
            color = (255, 0, 0)
        elif self.mode == "sand":
            color = (194, 178, 128)
        elif self.mode == "rock":
            color = (128, 128, 128)
        pygame.draw.rect(window, color, (col * self.node_size, row * self.node_size, brush_visual_size, brush_visual_size))
        
simulation = Simulation(window_width, window_height, node_size)

simulation.add_particle(0,0)
simulation.add_particle(1,1)


simulation.remove_particle(0,0)


#main loop
while True:
    #event handling
    #loops som tjekker for events, i dette tilfælde om brugeren har klikket på krydset for at lukke vinduet, og hvis det er tilfældet, så lukker programmet ned
    simulation.handle_controls()
 
    #draw stuff
    window.fill(grey)
    simulation.draw(window)

    # opdaterer displayet og sætter fps
    simulation.update()
    pygame.display.flip()
    clock.tick(fps)
