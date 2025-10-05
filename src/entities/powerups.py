# src/entities/powerups.py
import pygame
import math
from src.config import Config

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.image = self._create_powerup_surface()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Movimento
        self.speed = 2  # Velocidade de queda
        self.float_offset = 0
        self.float_speed = 0.1
        self.original_x = x  # Guarda posição X original para movimento de onda
        
        # Duração do efeito (em milissegundos)
        self.effect_duration = {
            'double_shot': 10000,  # 10 segundos
            'triple_shot': 8000,   # 8 segundos
            'shield': 12000,       # 12 segundos
            'speed': 15000         # 15 segundos
        }
    
    def _create_powerup_surface(self):
        size = 30
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Cores diferentes para cada tipo
        colors = {
            'double_shot': (255, 50, 50),    # Vermelho
            'triple_shot': (255, 100, 50),   # Laranja
            'shield': (50, 150, 255),        # Azul
            'speed': (50, 255, 50)           # Verde
        }
        
        base_color = colors.get(self.type, (255, 255, 255))
        glow_color = tuple(min(255, c + 100) for c in base_color)
        
        # Desenha o power-up com efeito de brilho
        if self.type in ['double_shot', 'triple_shot']:
            # Forma de projétil
            points = [
                (size//2, 0),
                (0, size),
                (size//2, size*3//4),
                (size, size)
            ]
            # Brilho
            pygame.draw.polygon(surface, glow_color, points)
            # Base
            smaller_points = [(x + 2 if i % 2 == 0 else x - 2, y + 2 if i % 2 == 1 else y - 2) 
                            for i, (x, y) in enumerate(points)]
            pygame.draw.polygon(surface, base_color, smaller_points)
            
        elif self.type == 'shield':
            # Forma circular com brilho
            pygame.draw.circle(surface, glow_color, (size//2, size//2), size//2)
            pygame.draw.circle(surface, base_color, (size//2, size//2), size//2 - 2)
            pygame.draw.circle(surface, glow_color, (size//2, size//2), size//4)
            
        elif self.type == 'speed':
            # Forma de raio
            points = [
                (size//2, 0),
                (size//4, size//2),
                (size//2, size//2),
                (size//4, size),
                (size*3//4, size//2),
                (size//2, size//2)
            ]
            # Brilho
            pygame.draw.polygon(surface, glow_color, points)
            # Base
            smaller_points = [(x + 1 if i % 2 == 0 else x - 1, y + 1 if i % 2 == 1 else y - 1) 
                            for i, (x, y) in enumerate(points)]
            pygame.draw.polygon(surface, base_color, smaller_points)
        
        return surface
    
    def update(self):
        # Movimento para baixo
        self.rect.y += self.speed
        
        # Movimento de onda horizontal
        self.float_offset += self.float_speed
        self.rect.centerx = self.original_x + math.sin(self.float_offset) * 30
        
        # Rotação do power-up (efeito visual)
        self.image = pygame.transform.rotate(self._create_powerup_surface(), 
                                          math.sin(self.float_offset) * 15)
        
        # Atualiza o rect para centralizar após rotação
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Remove se sair da tela
        if self.rect.top > Config.SCREEN_HEIGHT:
            self.kill()
    
    def apply_effect(self, player):
        """Aplica o efeito do power-up no jogador"""
        player.activate_powerup(self.type, self.effect_duration[self.type])