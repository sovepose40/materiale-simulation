import pygame,sys

#starter pygame
pygame.init()

#definere variabler
window_width = 800
window_height = 600
node_size = 50
fps = 120
grey = (29, 29, 29)
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
                pygame.draw.rect(window, light_grey, (col * self.node_size, row * self.node_size, self.node_size-1, self.node_size-1))
grid = Grid(window_width, window_height, node_size)



#main loop
while True:
    #event handling
    #loops som tjekker for events, i dette tilfælde om brugeren har klikket på krydset for at lukke vinduet, og hvis det er tilfældet, så lukker programmet ned
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #update stuff

    #draw stuff
    window.fill(grey)
    grid.draw(window)   


    # opdaterer displayet og sætter fps
    pygame.display.flip()
    clock.tick(fps)
