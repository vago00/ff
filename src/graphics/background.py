# src/graphics/background.py
import random
import math
import pygame
from src.config import Config

class Star:
    def __init__(self, layer):
        self.layer = layer  # 0=fundo, 1=meio, 2=frente
        self.reset()
        self.y = random.randrange(Config.SCREEN_HEIGHT)
        self.original_size = self.size
        self.warp_effect = 0
        
        # Define características baseadas na camada
        if self.layer == 0:  # Estrelas distantes
            self.base_speed = random.uniform(0.5, 1)
            self.brightness = random.uniform(0.3, 0.5)
        elif self.layer == 1:  # Estrelas médias
            self.base_speed = random.uniform(2, 3)
            self.brightness = random.uniform(0.5, 0.7)
        else:  # Estrelas próximas
            self.base_speed = random.uniform(4, 6)
            self.brightness = random.uniform(0.7, 1.0)
        
        self.speed = self.base_speed
        self.pulse_offset = random.random() * math.pi * 2
        
    def reset(self):
        self.x = random.randrange(Config.SCREEN_WIDTH)
        self.y = -10
        self.size = random.randint(1, 1 + self.layer)
        
    def update(self, game_state, volume, time):
        # Atualiza velocidade baseado no estado
        if game_state == "intense":
            target_speed = self.base_speed * (2.5 + self.layer)
            self.warp_effect = min(1.0, self.warp_effect + 0.1)
        else:
            target_speed = self.base_speed
            self.warp_effect = max(0.0, self.warp_effect - 0.1)
        
        self.speed = self.speed * 0.9 + target_speed * 0.1
        
        # Movimento vertical
        self.y += self.speed
        
        # Reinicia quando sai da tela
        if self.y > Config.SCREEN_HEIGHT:
            self.reset()
        
        # Efeito de pulso baseado no volume
        pulse = (math.sin(time * 0.005 + self.pulse_offset) + 1) * 0.5
        self.brightness = (0.3 + self.layer * 0.2) + volume * pulse
    
    def draw(self, surface):
        # Calcula cor baseada no brilho
        color_value = min(255, int(255 * self.brightness))
        
        # Cores diferentes por camada para efeito neon
        if self.layer == 0:
            color = (color_value, color_value, color_value)  # Branco
        elif self.layer == 1:
            color = (color_value, color_value * 0.8, color_value)  # Azulado
        else:
            color = (color_value, color_value * 0.6, color_value)  # Mais azul
        
        # Efeito de warp (alongamento)
        if self.warp_effect > 0:
            warp_length = int(self.speed * self.warp_effect * 2)
            start_pos = (int(self.x), int(self.y))
            end_pos = (int(self.x), int(self.y - warp_length))
            pygame.draw.line(surface, color, start_pos, end_pos, self.size)
        else:
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

class Nebula:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.randrange(Config.SCREEN_WIDTH)
        self.y = random.randrange(Config.SCREEN_HEIGHT)
        self.size = random.randrange(100, 300)
        self.color = self._generate_color()
        self.alpha = random.randint(30, 50)
        self.pulse_speed = random.uniform(0.001, 0.003)
        self.time_offset = random.random() * math.pi * 2
        
    def _generate_color(self):
        # Cores para nebulosas (tons de roxo, azul e rosa)
        colors = [
            (147, 39, 143),  # Roxo
            (64, 84, 178),   # Azul
            (191, 64, 191),  # Rosa
            (75, 0, 130),    # Índigo
        ]
        return random.choice(colors)
    
    def update(self, game_state, volume, time):
        # Pulso suave na transparência
        pulse = (math.sin(time * self.pulse_speed + self.time_offset) + 1) * 0.5
        self.alpha = 30 + int(20 * pulse) + int(volume * 20)
        
        # Move lentamente para baixo
        self.y += 0.2
        if self.y - self.size > Config.SCREEN_HEIGHT:
            self.reset()
    
    def draw(self, surface):
        # Cria superfície com transparência
        nebula_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Desenha gradiente circular
        for radius in range(self.size, 0, -2):
            alpha = int(self.alpha * (radius / self.size))
            color = (*self.color, alpha)
            pygame.draw.circle(nebula_surface, color, (self.size, self.size), radius)
        
        # Desenha na superfície principal
        surface.blit(nebula_surface, (self.x - self.size, self.y - self.size))

class Supernova:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1
        self.max_size = random.randint(100, 200)
        self.growth_speed = random.uniform(5, 10)
        self.alpha = 255
        
    def update(self):
        self.size = min(self.size + self.growth_speed, self.max_size)
        if self.size >= self.max_size:
            self.alpha = max(0, self.alpha - 10)
        return self.alpha > 0
    
    def draw(self, surface):
        if self.alpha <= 0:
            return
            
        # Cria superfície com transparência
        nova_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Cores em camadas para efeito de explosão
        colors = [
            (255, 255, 255, self.alpha),      # Branco central
            (255, 200, 100, self.alpha // 2),  # Amarelo
            (255, 100, 50, self.alpha // 3)    # Laranja
        ]
        
        for i, color in enumerate(colors):
            radius = int(self.size * (1 - i * 0.2))
            pygame.draw.circle(nova_surface, color, (self.size, self.size), radius)
        
        surface.blit(nova_surface, (self.x - self.size, self.y - self.size))

class Background:
    def __init__(self):
        # Cria estrelas em diferentes camadas
        self.stars = []
        self.stars.extend([Star(0) for _ in range(50)])  # Camada distante
        self.stars.extend([Star(1) for _ in range(30)])  # Camada média
        self.stars.extend([Star(2) for _ in range(20)])  # Camada próxima
        
        # Nebulosas
        self.nebulas = [Nebula() for _ in range(3)]
        
        # Supernovas
        self.supernovas = []
        self.last_nova_time = 0
        self.nova_delay = 5000  # 5 segundos entre supernovas
    
    def update(self, game_state, volume=0):
        current_time = pygame.time.get_ticks()
        
        # Atualiza estrelas
        for star in self.stars:
            star.update(game_state, volume, current_time)
        
        # Atualiza nebulosas
        for nebula in self.nebulas:
            nebula.update(game_state, volume, current_time)
        
        # Atualiza e remove supernovas mortas
        self.supernovas = [nova for nova in self.supernovas if nova.update()]
        
        # Chance de criar nova supernova
        if (current_time - self.last_nova_time > self.nova_delay and 
            random.random() < 0.01 + (volume * 0.1)):
            x = random.randrange(Config.SCREEN_WIDTH)
            y = random.randrange(Config.SCREEN_HEIGHT)
            self.supernovas.append(Supernova(x, y))
            self.last_nova_time = current_time
    
    def draw(self, surface):
        # Desenha nebulosas primeiro (fundo)
        for nebula in self.nebulas:
            nebula.draw(surface)
        
        # Desenha estrelas por camada (profundidade)
        for star in sorted(self.stars, key=lambda x: x.layer):
            star.draw(surface)
        
        # Desenha supernovas por cima
        for nova in self.supernovas:
            nova.draw(surface)