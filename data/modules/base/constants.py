import pygame.event

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

SCALE = 5
TILE_SIZE = 16 * SCALE

START_EVENT = pygame.event.Event(pygame.event.custom_type())
WIN_EVENT = pygame.event.Event(pygame.event.custom_type())
RESTART_EVENT = pygame.event.Event(pygame.event.custom_type())
