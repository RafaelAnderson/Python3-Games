import pygame
import sys
import time

ANCHO = 640
ALTO = 480
color_negro = (0, 0, 0) # Color negro RGB
color_blanco = (255, 255, 255) # Color blanco RGB
color_rojo = (255, 0, 0) # Color rojo RGB

#####

class Escena:
    def __init__(self):
        "Inicializacion"
        self.proximaEscena = False
        self.jugando = True
        pass
    def leer_eventos(self, eventos):
        "Lee la lista de todos los eventos."
        pass

    def actualizar(self):
        "Cálculos y lógica."
        pass

    def dibujar(self, pantalla):
        "Dibuja los objetos en pantalla."
        pass

    def cambiar_escena(self, escena):
        "Selecciona la nueva escena a ser desplegada"
        self.proximaEscena = escena

class Director:
    def __init__(self, titulo = "", res = (ANCHO, ALTO)):
        pygame.init()
        # Inicializando pantalla.
        self.pantalla = pygame.display.set_mode(res)
        # Configurar título de pantalla.
        pygame.display.set_caption(titulo)
        # Crear el reloj.
        self.reloj = pygame.time.Clock()
        self.escena = None
        self.escenas = {}

    def ejecutar(self, escena_inicial, fps = 60):
        self.escena = self.escenas[escena_inicial]
        jugando = True
        while jugando:
            self.reloj.tick(fps)
            eventos = pygame.event.get()
            # Revisar todos los eventos.
            for evento in eventos:
                # Si se presiona la tachita de la barra de título,
                if evento.type == pygame.QUIT:
                    # cerrar el videojuego.
                    jugando = False

            self.escena.leer_eventos(eventos)
            self.escena.actualizar()
            self.escena.dibujar(self.pantalla)

            self.elegirEscena(self.escena.proximaEscena)

            if jugando:
                jugando = self.escena.jugando

            pygame.display.flip()

        time.sleep(3)

    def elegirEscena(self, proximaEscena):
        if proximaEscena:
            if proximaEscena not in self.escenas:
                self.agregarEscena(proximaEscena)
            self.escena = self.escenas[proximaEscena]

    def agregarEscena(self, escena):
        escenaClase = 'Escena'+escena
        escenaObj = globals()[escenaClase]
        self.escenas[escena] = escenaObj();


class EscenaNivel1(Escena):
    def __init__(self):
        Escena.__init__(self)

        self.pelota = Pelota()
        self.jugador = Jugador()
        self.muro = Muro(48)

        self.puntuacion = 0
        self.vidas = 3
        self.esperando_saque = True

        # Repetición de evento de tecla presionada
        pygame.key.set_repeat(30)

    def leer_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.jugador.update(evento)
                if self.esperando_saque == True and evento.key == pygame.K_SPACE:
                    self.esperando_saque = False
                    if self.pelota.rect.centerx < ANCHO / 2:
                        self.pelota.speed = [3, -3]
                    else:
                        self.pelota.speed = [-3, -3]

    def actualizar(self):
        if self.esperando_saque == False:
            # Actualizar posicion de la pelota
            self.pelota.update()
        else:
            self.pelota.rect.midbottom = self.jugador.rect.midtop
        # Colision entre pelota y jugador
        if pygame.sprite.collide_rect(self.pelota, self.jugador):
            self.pelota.speed[1] = -self.pelota.speed[1]
        # Colision de la pelota con el muro
        lista = pygame.sprite.spritecollide(self.pelota, self.muro, False)
        if lista:
            ladrillo = lista[0]
            cx = self.pelota.rect.centerx
            if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
                self.pelota.speed[0] = -self.pelota.speed[0]
            else:
                self.pelota.speed[1] = -self.pelota.speed[1]
            self.muro.remove(ladrillo)
            self.puntuacion += 20
        # Revisar si la pelota sale de la pantalla
        if self.pelota.rect.top > ALTO:
            self.vidas -= 1
            self.esperando_saque = True

        if self.vidas <= 0:
            self.cambiar_escena('JuegoTerminado')

    def dibujar(self, pantalla):
        # Rellenar fondo
        pantalla.fill(color_negro)
        # Mostrar puntuación
        self.mostrar_puntuacion(pantalla)
        self.mostrar_vidas(pantalla)
        # Dibujar pelota (blit dibuja una superficie sobre otra)
        pantalla.blit(self.pelota.image, self.pelota.rect)
        pantalla.blit(self.jugador.image, self.jugador.rect)
        # Dibujar los ladrillos
        self.muro.draw(pantalla)

    def mostrar_puntuacion(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        texto = fuente.render(str(self.puntuacion).zfill(5), True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.topleft = [0, 0]
        pantalla.blit(texto, texto_rect)

    def mostrar_vidas(self, pantalla):
        fuente = pygame.font.SysFont('Consolas', 20)
        cadena = "Vidas: " + str(self.vidas).zfill(2)
        texto = fuente.render(cadena, True, color_rojo)
        texto_rect = texto.get_rect()
        texto_rect.topright = [ANCHO, 0]
        pantalla.blit(texto, texto_rect)

class EscenaJuegoTerminado(Escena):
    def actualizar(self):
        self.jugando = False

    def dibujar(self, pantalla):
        fuente = pygame.font.SysFont('Arial', 72)
        texto = fuente.render('Juego terminado :(', True, color_blanco)
        texto_rect = texto.get_rect()
        texto_rect.center = [ANCHO / 2, ALTO / 2]
        pantalla.blit(texto, texto_rect)


#####

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
        self.speed = [0, 0]

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


director = Director('Break Out by RAPG', (ANCHO, ALTO))
director.agregarEscena('Nivel1')
director.ejecutar('Nivel1')

##########################################################