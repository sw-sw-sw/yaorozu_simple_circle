import pygame
from config import *

class PygameRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def draw(self, positions):
        self.screen.fill(BACKGROUND_COLOR)
        for pos in positions:
            pygame.draw.circle(self.screen, AGENT_COLOR, (int(pos[0]), int(pos[1])), AGENT_RADIUS, 1)

        
        pygame.display.flip()
