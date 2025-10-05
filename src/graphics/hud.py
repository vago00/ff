# src/graphics/hud.py
import pygame
from src.config import Config

class HUD:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Cores
        self.HEALTH_BG = (60, 60, 60)
        self.HEALTH_FG = (220, 50, 50)
        self.SCORE_COLOR = (255, 255, 255)
        self.MULTIPLIER_COLOR = (255, 215, 0)  # Dourado
        
        # Dimensões da barra de vida
        self.health_width = 200
        self.health_height = 20
        self.health_border = 2
    
    def draw_health_bar(self, surface, current_health, max_health):
        # Posição da barra de vida
        x = 20
        y = Config.SCREEN_HEIGHT - 40
        
        # Borda/Background
        pygame.draw.rect(surface, self.HEALTH_BG, 
                        (x, y, self.health_width, self.health_height))
        
        # Barra de vida
        health_percent = current_health / max_health
        current_width = int(self.health_width * health_percent)
        pygame.draw.rect(surface, self.HEALTH_FG,
                        (x, y, current_width, self.health_height))
        
        # Texto de vida
        health_text = f"{current_health}/{max_health}"
        text_surf = self.font_small.render(health_text, True, self.SCORE_COLOR)
        text_rect = text_surf.get_rect(midleft=(x + self.health_width + 10, y + self.health_height/2))
        surface.blit(text_surf, text_rect)
    
    def draw_score(self, surface, score, high_score, multiplier):
        # Score atual
        score_text = f"Score: {score}"
        score_surf = self.font_normal.render(score_text, True, self.SCORE_COLOR)
        surface.blit(score_surf, (20, 20))
        
        # High score
        high_score_text = f"High Score: {high_score}"
        high_score_surf = self.font_small.render(high_score_text, True, self.SCORE_COLOR)
        surface.blit(high_score_surf, (20, 60))
        
        # Multiplicador
        if multiplier > 1.0:
            mult_text = f"x{multiplier:.1f}"
            mult_surf = self.font_normal.render(mult_text, True, self.MULTIPLIER_COLOR)
            surface.blit(mult_surf, (Config.SCREEN_WIDTH - 100, 20))
    
    def draw_game_over(self, surface, final_score):
        # Escurece a tela
        overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        surface.blit(overlay, (0, 0))
        
        # Texto de Game Over
        game_over_text = "GAME OVER"
        game_over_surf = self.font_big.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2 - 50))
        
        # Pontuação final
        score_text = f"Final Score: {final_score}"
        score_surf = self.font_normal.render(score_text, True, self.SCORE_COLOR)
        score_rect = score_surf.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2 + 20))
        
        # Instrução para reiniciar
        restart_text = "Press SPACE to restart"
        restart_surf = self.font_small.render(restart_text, True, self.SCORE_COLOR)
        restart_rect = restart_surf.get_rect(center=(Config.SCREEN_WIDTH/2, Config.SCREEN_HEIGHT/2 + 80))
        
        # Desenha todos os elementos
        surface.blit(game_over_surf, game_over_rect)
        surface.blit(score_surf, score_rect)
        surface.blit(restart_surf, restart_rect)
    
    def draw(self, surface, game_state):
        # Desenha elementos básicos do HUD
        self.draw_health_bar(surface, game_state.current_health, game_state.max_health)
        self.draw_score(surface, game_state.score, game_state.high_score, game_state.multiplier)
        
        # Se game over, desenha tela de game over
        if game_state.game_over:
            self.draw_game_over(surface, game_state.score)