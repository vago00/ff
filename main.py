# main.py
import pygame
import random
from src.config import Config
from src.audio.analyzer import AudioAnalyzer
from src.entities.player import Player
from src.entities.enemies import EnemySpawner
from src.graphics.background import Background
from src.graphics.particles import ParticleSystem
from src.graphics.hud import HUD
from src.states.game_state import GameState
from src.systems.powerup_spawner import PowerUpSpawner

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter Audio-Reativo")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sistema de estado do jogo
        self.game_state = GameState()
        
        # Sistema de áudio
        self.audio = AudioAnalyzer()
        
        # Grupos de sprites
        self.projectiles = pygame.sprite.Group()
        self.player = Player(self.projectiles)
        self.all_sprites = pygame.sprite.Group(self.player)
        
        # Sistema de inimigos
        self.enemy_spawner = EnemySpawner()
        
        # Sistema de power-ups
        self.powerup_spawner = PowerUpSpawner()
        
        # Sistemas gráficos
        self.background = Background()
        self.particle_system = ParticleSystem()
        self.hud = HUD()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state.game_over:
                    self.reset_game()
    
    def check_collisions(self):
        # Colisões entre projéteis e inimigos
        hits = pygame.sprite.groupcollide(
            self.projectiles, 
            self.enemy_spawner.enemies, 
            True,  # Remove projétil
            True   # Remove inimigo
        )
        
        # Processa hits e adiciona pontos
        for proj, enemies in hits.items():
            for enemy in enemies:
                # Adiciona pontos baseado no tipo de inimigo
                points = 10  # Pontos base
                if enemy.enemy_type == "elite":
                    points = 20
                elif enemy.enemy_type == "boss":
                    points = 50
                
                # Adiciona pontos com multiplicador
                self.game_state.add_score(points, self.audio.get_state())
                
                # Efeitos visuais
                self.particle_system.create_explosion(
                    enemy.rect.centerx,
                    enemy.rect.centery,
                    (255, 200, 0)
                )
                self.particle_system.create_hit_sparks(
                    enemy.rect.centerx,
                    enemy.rect.centery
                )
                
                # Chance de dropar power-up ao destruir inimigo
                if random.random() < 0.1:  # 10% de chance
                    self.powerup_spawner.spawn_specific(
                        random.choice(['double_shot', 'triple_shot', 'shield', 'speed']),
                        enemy.rect.centerx,
                        enemy.rect.centery
                    )
        
        # Colisões entre jogador e power-ups
        powerup_type = self.powerup_spawner.check_collisions(self.player)
        if powerup_type:
            # Efeito visual ao pegar power-up
            self.particle_system.create_powerup_effect(
                self.player.rect.centerx,
                self.player.rect.centery,
                powerup_type
            )
        
        # Colisões entre jogador e inimigos (se não tiver escudo)
        if not self.player.shield_active:
            hits = pygame.sprite.spritecollide(self.player, self.enemy_spawner.enemies, True)
            if hits:
                self.game_state.take_damage(25)  # 25 de dano por colisão
    
    def update(self):
        if not self.game_state.game_over:
            game_state = self.audio.get_state()
            
            # Atualiza todos os elementos
            self.all_sprites.update(game_state)
            self.projectiles.update()
            self.enemy_spawner.update(game_state, self.audio.volume)
            self.powerup_spawner.update(game_state, self.audio.get_state(), self.audio.volume)
            self.background.update(game_state)
            self.particle_system.update()
            
            # Adiciona fogo dos motores
            if random.random() < 0.3:
                self.particle_system.create_engine_fire(
                    self.player.rect.centerx - 10,
                    self.player.rect.bottom
                )
                self.particle_system.create_engine_fire(
                    self.player.rect.centerx + 10,
                    self.player.rect.bottom
                )
            
            # Verifica colisões
            self.check_collisions()
    
    def draw(self):
        self.screen.fill(Config.BLACK)
        
        # Desenha elementos do jogo
        self.background.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.enemy_spawner.enemies.draw(self.screen)
        self.powerup_spawner.powerups.draw(self.screen)
        
        # Desenha jogador por último para ficar sobre os outros elementos
        self.player.draw(self.screen)
        
        # Desenha partículas por cima de tudo
        self.particle_system.draw(self.screen)
        
        # Desenha HUD
        self.hud.draw(self.screen, self.game_state)
        
        pygame.display.flip()
    
    def reset_game(self):
        """Reinicia o jogo após game over"""
        self.game_state.reset()
        
        # Limpa todos os sprites
        self.projectiles.empty()
        self.enemy_spawner.enemies.empty()
        self.powerup_spawner.clear()
        
        # Reposiciona o jogador
        self.player.rect.centerx = Config.SCREEN_WIDTH // 2
        self.player.rect.bottom = Config.SCREEN_HEIGHT - 20
    
    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(Config.FPS)
        finally:
            self.audio.stop()
            pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()