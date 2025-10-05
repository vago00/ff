# src/systems/powerup_spawner.py
import pygame
import random
from src.config import Config
from src.entities.powerups import PowerUp

class PowerUpSpawner:
    def __init__(self):
        self.powerups = pygame.sprite.Group()
        self.last_spawn_time = 0
        
        # Configurações de spawn
        self.base_spawn_delay = 5000  # 5 segundos base entre spawns
        self.min_spawn_delay = 2000   # Mínimo de 2 segundos entre spawns
        self.spawn_chance = 0.1       # 10% chance base de spawn
        
        # Weights para cada tipo de power-up
        self.powerup_weights = {
            'double_shot': 40,  # 40% chance
            'triple_shot': 20,  # 20% chance
            'shield': 20,       # 20% chance
            'speed': 20         # 20% chance
        }
    
    def update(self, game_state, audio_state, audio_volume):
        current_time = pygame.time.get_ticks()
        
        # Ajusta chance de spawn baseado no estado do áudio
        if audio_state == "void":
            spawn_chance = self.spawn_chance * 0.5
        elif audio_state == "ambient":
            spawn_chance = self.spawn_chance
        else:  # intense
            spawn_chance = self.spawn_chance * 2
        
        # Aumenta chance baseado no volume
        spawn_chance += audio_volume * 0.2
        
        # Ajusta delay baseado no estado
        spawn_delay = self.base_spawn_delay
        if audio_state == "intense":
            spawn_delay = self.base_spawn_delay * 0.5
        
        # Tenta spawnar novo power-up
        if (current_time - self.last_spawn_time > spawn_delay and 
            random.random() < spawn_chance):
            self._spawn_powerup(audio_state)
            self.last_spawn_time = current_time
        
        # Atualiza power-ups existentes
        self.powerups.update()
    
    def _spawn_powerup(self, audio_state):
        # Posição aleatória no topo da tela
        x = random.randint(50, Config.SCREEN_WIDTH - 50)
        y = -30  # Acima da tela
        
        # Ajusta weights baseado no estado do áudio
        weights = self.powerup_weights.copy()
        if audio_state == "intense":
            # Aumenta chance de power-ups mais poderosos
            weights['triple_shot'] += 20
            weights['shield'] += 10
        
        # Escolhe tipo baseado nos weights
        total = sum(weights.values())
        r = random.uniform(0, total)
        cumsum = 0
        
        for powerup_type, weight in weights.items():
            cumsum += weight
            if r <= cumsum:
                powerup = PowerUp(x, y, powerup_type)
                self.powerups.add(powerup)
                break
    
    def spawn_specific(self, powerup_type, x, y):
        """Spawna um power-up específico em uma posição específica"""
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.add(powerup)
    
    def check_collisions(self, player):
        """Verifica colisões com o jogador e aplica efeitos"""
        hits = pygame.sprite.spritecollide(player, self.powerups, True)
        for powerup in hits:
            powerup.apply_effect(player)
            return powerup.type
        return None
    
    def get_active_powerups(self):
        """Retorna a quantidade de power-ups ativos"""
        return len(self.powerups)
    
    def clear(self):
        """Remove todos os power-ups ativos"""
        self.powerups.empty()