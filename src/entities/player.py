# src/entities/player.py
import pygame
import math
from src.config import Config
from src.entities.projectiles import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, projectiles_group):
        super().__init__()
        self.image = self._create_ship_surface()
        self.rect = self.image.get_rect()
        self.rect.centerx = Config.SCREEN_WIDTH // 2
        self.rect.bottom = Config.SCREEN_HEIGHT - 20
        
        # Características base
        self.base_speed = 5
        self.speed = self.base_speed
        self.projectiles_group = projectiles_group
        
        # Sistema de tiro
        self.shoot_delay = 250
        self.last_shot = 0
        self.shot_type = 'single'
        
        # Power-ups ativos
        self.active_powerups = {}
        self.shield_active = False
        self.shield_alpha = 255
        
        # Surface do escudo
        self.shield_surface = self._create_shield_surface()
    
    def _create_ship_surface(self):
        """Cria a superfície da nave"""
        # Tamanho maior para mais detalhes
        surface = pygame.Surface((60, 80), pygame.SRCALPHA)
        
        # Cores
        RED = (220, 20, 20)        # Vermelho mais escuro
        DARK_RED = (180, 10, 10)   # Vermelho ainda mais escuro
        GOLD = (255, 215, 0)       # Dourado para detalhes
        GRAY = (80, 80, 80)        # Cinza para partes metálicas
        
        # Corpo principal (forma de asa)
        points = [
            (30, 0),    # Ponta
            (0, 60),    # Base esquerda
            (10, 70),   # Entalhe esquerdo
            (50, 70),   # Entalhe direito
            (60, 60),   # Base direita
        ]
        pygame.draw.polygon(surface, RED, points)
        
        # Contorno do corpo
        pygame.draw.polygon(surface, DARK_RED, points, 2)
        
        # Asas laterais
        left_wing = [
            (5, 40),
            (0, 60),
            (20, 55)
        ]
        right_wing = [
            (55, 40),
            (60, 60),
            (40, 55)
        ]
        pygame.draw.polygon(surface, DARK_RED, left_wing)
        pygame.draw.polygon(surface, DARK_RED, right_wing)
        
        # Motores (retângulos na base)
        pygame.draw.rect(surface, GRAY, (15, 65, 10, 15))
        pygame.draw.rect(surface, GRAY, (35, 65, 10, 15))
        
        # Detalhes dourados (círculos e linhas)
        pygame.draw.circle(surface, GOLD, (30, 30), 8)
        pygame.draw.circle(surface, GOLD, (30, 30), 8, 1)
        pygame.draw.line(surface, GOLD, (10, 50), (50, 50), 2)
        
        return surface
    
    def _create_shield_surface(self):
        """Cria a superfície do escudo"""
        size = max(self.rect.width, self.rect.height) + 20
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        # Círculo externo com gradiente
        for radius in range(size//2, size//2 - 4, -1):
            alpha = int(255 * (radius - (size//2 - 4)) / 4)
            pygame.draw.circle(surface, (50, 150, 255, alpha), (center, center), radius)
        
        return surface
    
    def update(self, game_state):
        now = pygame.time.get_ticks()
        
        # Atualiza power-ups ativos
        expired_powerups = []
        for effect, end_time in self.active_powerups.items():
            if now >= end_time:
                expired_powerups.append(effect)
                self._remove_powerup_effect(effect)
        
        for effect in expired_powerups:
            del self.active_powerups[effect]
        
        # Atualiza movimento
        self._handle_movement()
        
        # Atualiza tiro
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self._handle_shooting(game_state)
        
        # Efeito pulsante do escudo
        if self.shield_active:
            self.shield_alpha = 128 + int(127 * math.sin(now * 0.01))
    
    def _handle_movement(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < Config.SCREEN_WIDTH:
            self.rect.x += self.speed
    
    def _handle_shooting(self, game_state):
        now = pygame.time.get_ticks()
        
        if now - self.last_shot > self.shoot_delay:
            if self.shot_type == 'single':
                self._shoot_single()
            elif self.shot_type == 'double':
                self._shoot_double()
            elif self.shot_type == 'triple':
                self._shoot_triple()
            
            self.last_shot = now
    
    def _shoot_single(self):
        """Tiro único central"""
        projectile = Projectile(self.rect.centerx, self.rect.top)
        self.projectiles_group.add(projectile)
    
    def _shoot_double(self):
        """Tiro duplo nas laterais"""
        offset = 10
        projectile1 = Projectile(self.rect.centerx - offset, self.rect.top)
        projectile2 = Projectile(self.rect.centerx + offset, self.rect.top)
        self.projectiles_group.add(projectile1, projectile2)
    
    def _shoot_triple(self):
        """Tiro triplo (centro e laterais)"""
        projectile1 = Projectile(self.rect.centerx, self.rect.top)
        projectile2 = Projectile(self.rect.centerx - 15, self.rect.top)
        projectile3 = Projectile(self.rect.centerx + 15, self.rect.top)
        self.projectiles_group.add(projectile1, projectile2, projectile3)
    
    def activate_powerup(self, powerup_type, duration):
        """Ativa um power-up por uma duração específica"""
        now = pygame.time.get_ticks()
        end_time = now + duration
        
        if powerup_type == 'double_shot':
            self.shot_type = 'double'
        elif powerup_type == 'triple_shot':
            self.shot_type = 'triple'
        elif powerup_type == 'shield':
            self.shield_active = True
        elif powerup_type == 'speed':
            self.speed = self.base_speed * 1.5
        
        self.active_powerups[powerup_type] = end_time
    
    def _remove_powerup_effect(self, powerup_type):
        """Remove o efeito de um power-up"""
        if powerup_type in ['double_shot', 'triple_shot']:
            self.shot_type = 'single'
        elif powerup_type == 'shield':
            self.shield_active = False
        elif powerup_type == 'speed':
            self.speed = self.base_speed
    
    def draw(self, surface):
        """Sobrescreve o método draw para incluir o escudo"""
        # Desenha a nave
        surface.blit(self.image, self.rect)
        
        # Desenha o escudo se ativo
        if self.shield_active:
            shield = self.shield_surface.copy()
            shield.set_alpha(self.shield_alpha)
            shield_rect = shield.get_rect(center=self.rect.center)
            surface.blit(shield, shield_rect)