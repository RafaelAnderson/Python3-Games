import pygame
import sys

ANCHO = 640
ALTO = 480

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar imagen
        self.image = pygame.image.load("images/pelota.png")
        # Obtener rectángulo
        self.rect = self.image.get_rect()
        # Posicion inicial
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2

# Inicializando pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#Configurando título
pygame.display.set_caption('Break Out')

# Objeto pelota
pelota = Pelota()

while True:
    #Revisando eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()

    # Dibujar pelota
    pantalla.blit(pelota.image, pelota.rect)

    # Actualiza elementos de la pantalla
    pygame.display.flip()