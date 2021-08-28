import pygame
import sys

ANCHO = 640
ALTO = 480
color_negro = (0, 0, 0) # Color RGB

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
        #Velocidad
        self.speed = [3, 3]
    def update(self):
        # Evitar que salga por abajo y arriba
        if self.rect.bottom >= ALTO or self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que salga por la derecha e izquierda
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        self.rect.move_ip(self.speed)

# Creando Barra
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/barra.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        self.speed = [3, 0]
    def update(self, evento):
        # Flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [5, 0]
        else: self.speed = [0, 0]
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        #Cargar imagen
        self.image = pygame.image.load("images/ladrillo.png")
        # Obtener rectángulo
        self.rect = self.image.get_rect()
        #Posicion inicial, provista externamente
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)
        pos_x = 0
        pos_y = 20

        for i in range (cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)
            pos_x += ladrillo.rect.width

##########################################################

# Inicializando pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
#Configurando título
pygame.display.set_caption('Break Out')
# Creando el reloj
reloj = pygame.time.Clock()
# Objeto pelota
pelota = Pelota()
jugador = Jugador()
muro = Muro(10)
# Repetición de evento de tecla presionada
pygame.key.set_repeat(30)

################### JUEGO ####################
while True:
    # Estableciendo frames
    reloj.tick(75)
    #Revisando eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)

    #Actualizar posicion de la pelota
    pelota.update()
    #Colision entre pelota y jugador
    if pygame.sprite.collide_rect(pelota, jugador):
        pelota.speed[1] = -pelota.speed[1]
    #Colision de la pelota con el muro
    lista = pygame.sprite.spritecollide(pelota, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = pelota.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            pelota.speed[0] = -pelota.speed[0]
        else:
            pelota.speed[1] = -pelota.speed[1]
        muro.remove(ladrillo)

    #Rellenar fondo
    pantalla.fill(color_negro)
    # Dibujar pelota (blit dibuja una superficie sobre otra)
    pantalla.blit(pelota.image, pelota.rect)
    pantalla.blit(jugador.image, jugador.rect)
    #Dibujar los ladrillos
    muro.draw(pantalla)
    # Actualiza elementos de la pantalla
    pygame.display.flip()