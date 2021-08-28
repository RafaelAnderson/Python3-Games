import sys
import pygame

ANCHO  = 640
ALTO = 480

# Inicializando pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
