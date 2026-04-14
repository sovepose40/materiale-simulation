import pygame,sys

#starter pygame
pygame.init()

window_width = 800
window_height = 600
fps = 120

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Materiale Simulation")

clock = pygame.time.Clock()

#gameplay loop
while True:
    pygame.display.flip()
    clock.tick(fps)
