# src/entities/projectiles.py
import pygame
from src.config import Config

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, game_state="ambient"):
        super().__init__()
        self.image = self._create_projectile_surface(game_state)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Negativo para ir para cima
        
    def _create_projectile_surface(self, game_state):
        # Diferentes tipos de tiro baseado no estado do jogo
        if game_state == "void":
            # Tiro básico (azul pequeno)
            surface = pygame.Surface((4, 10), pygame.SRCALPHA)
            pygame.draw.rect(surface, (0, 255, 255), (0, 0, 4, 10))
            
        elif game_state == "ambient":
            # Tiro médio (vermelho)
            surface = pygame.Surface((6, 15), pygame.SRCALPHA)
            pygame.draw.rect(surface, (255, 50, 50), (0, 0, 6, 15))
            
        else:  # intense
            # Tiro grande (dourado)
            surface = pygame.Surface((8, 20), pygame.SRCALPHA)
            pygame.draw.rect(surface, (255, 215, 0), (0, 0, 8, 20))
            
        return surface
    
    def update(self):
        self.rect.y += self.speed
        # Remove o projétil quando sair da tela
        if self.rect.bottom < 0:
            self.kill()