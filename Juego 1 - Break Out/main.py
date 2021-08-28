import pygame
import sys
import time

ANCHO = 640
ALTO = 480
color_negro = (0, 0, 0) # Color negro RGB
color_blanco = (255, 255, 255) # Color blanco RGB
color_rojo = (255, 0, 0) # Color rojo RGB
esperando_saque = True

# Inicializar fuentes en el videojuego
pygame.init()

class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar imagen
        self.image = pygame.image.load("images/pelota.png")
        # Obtener rectángulo
        self.rect = self.image.get_rect()
        # Posicion inicial
        self.rect.centerx = int(ANCHO / 2 - 40)
        self.rect.centery = int(ALTO / 2)
        #Velocidad
        self.speed = [3, 3]
    def update(self):
        # Evitar que salga por abajo y arriba
        if self.rect.top <= 0:
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
        self.rect.midbottom = (int(ANCHO / 2), int(ALTO - 40))
        self.speed = [5, 0]
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
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height


def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 72)
    texto = fuente.render('Juego terminado :(', True, (color_blanco))
    texto_rect = texto.get_rect()
    texto_rect.center = [int(ANCHO / 2), int(ALTO / 2)]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Pausando por 3 segundos
    time.sleep(3)
    sys.exit()

def mostrar_puntuacion():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, (color_blanco))
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0,0]
    pantalla.blit(texto, texto_rect)

def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render("Vidas: " + str(vidas), True, (color_rojo))
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO,0]
    pantalla.blit(texto, texto_rect)

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
#Multiplo de 16
muro = Muro(48)
puntuacion = 0
vidas = 3
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
            if esperando_saque == True and evento.key == pygame.K_SPACE:
                esperando_saque = False
                if pelota.rect.centerx < int(ANCHO / 2):
                    pelota.speed = [3, -3]
                else:
                    pelota.speed = [-3, -3]

    if esperando_saque == False:
        #Actualizar posicion de la pelota
        pelota.update()
    else:
        pelota.rect.midbottom = jugador.rect.midtop
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
        puntuacion += 20
    # Revisar si la pelota sale de la pantalla
    if pelota.rect.top > ALTO:
        vidas -= 1
        esperando_saque = True

    # Rellenar fondo
    pantalla.fill(color_negro)
    #Mostrar puntuación
    mostrar_puntuacion()
    mostrar_vidas()
    # Dibujar pelota (blit dibuja una superficie sobre otra)
    pantalla.blit(pelota.image, pelota.rect)
    pantalla.blit(jugador.image, jugador.rect)
    # Dibujar los ladrillos
    muro.draw(pantalla)
    # Actualiza elementos de la pantalla
    pygame.display.flip()

    if vidas <= 0:
        juego_terminado()