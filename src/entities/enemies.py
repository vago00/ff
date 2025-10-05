# src/entities/enemies.py
import pygame
import random
import math
from src.config import Config

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="basic"):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = self._create_enemy_surface()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movimento
        self.speed = 2
        self.angle = 0
        self.wave_amplitude = 50
        self.original_x = x
        
    def _create_enemy_surface(self):
        size = 40
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.enemy_type == "basic":
            # Inimigo triangular básico (vermelho)
            color = (200, 30, 30)
            points = [(size//2, 0), (0, size), (size, size)]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (150, 20, 20), points, 2)
            
        elif self.enemy_type == "elite":
            # Inimigo hexagonal mais elaborado (dourado)
            color = (218, 165, 32)
            radius = size // 2
            points = []
            for i in range(6):
                angle = math.pi/3 * i
                x = radius + radius * math.cos(angle)
                y = radius + radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (255, 215, 0), points, 2)
            
        else:  # boss
            # Chefe maior e mais detalhado
            color = (180, 0, 0)
            pygame.draw.circle(surface, color, (size//2, size//2), size//2)
            pygame.draw.circle(surface, (255, 215, 0), (size//2, size//2), size//2, 2)
            pygame.draw.circle(surface, (255, 215, 0), (size//2, size//2), size//4)
        
        return surface
    
    def update(self, game_state):
        # Movimento básico para baixo
        self.rect.y += self.speed
        
        # Movimento ondulado
        self.angle += 0.05
        self.rect.x = self.original_x + math.sin(self.angle) * self.wave_amplitude
        
        # Ajusta velocidade baseado no estado do jogo
        if game_state == "void":
            self.speed = 1
        elif game_state == "ambient":
            self.speed = 2
        else:  # intense
            self.speed = 3
        
        # Remove inimigo se sair da tela
        if self.rect.top > Config.SCREEN_HEIGHT:
            self.kill()

class EnemySpawner:
    def __init__(self):
        self.last_spawn = 0
        self.spawn_delay = 1000  # 1 segundo entre spawns
        self.enemies = pygame.sprite.Group()
        
    def update(self, game_state, volume):
        now = pygame.time.get_ticks()
        
        # Ajusta frequência de spawn baseado no estado e volume
        spawn_chance = 0.1  # chance base
        if game_state == "void":
            spawn_chance = 0.05
        elif game_state == "intense":
            spawn_chance = 0.2
        
        # Aumenta chance baseado no volume
        spawn_chance += volume
        
        # Tenta criar novo inimigo
        if now - self.last_spawn > self.spawn_delay and random.random() < spawn_chance:
            self._spawn_enemy(game_state)
            self.last_spawn = now
            
        # Atualiza inimigos existentes
        self.enemies.update(game_state)
    
    def _spawn_enemy(self, game_state):
        # Posição aleatória no topo da tela
        x = random.randint(50, Config.SCREEN_WIDTH - 50)
        
        # Tipo de inimigo baseado no estado
        if game_state == "void":
            enemy_type = "basic"
        elif game_state == "ambient":
            enemy_type = random.choice(["basic", "elite"])
        else:  # intense
            enemy_type = random.choice(["basic", "elite", "boss"])
        
        enemy = Enemy(x, -50, enemy_type)
        self.enemies.add(enemy)