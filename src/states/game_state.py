# src/states/game_state.py
import json
import os

class GameState:
    def __init__(self):
        # Pontuação
        self.score = 0
        self.high_score = self.load_high_score()
        self.multiplier = 1.0
        
        # Sistema de vida
        self.max_health = 100
        self.current_health = self.max_health
        self.is_alive = True
        
        # Estado do jogo
        self.game_over = False
        self.level = 1
        
    def add_score(self, base_points, game_state):
        # Ajusta multiplicador baseado no estado do áudio
        if game_state == "void":
            self.multiplier = 1.0
        elif game_state == "ambient":
            self.multiplier = 1.5
        else:  # intense
            self.multiplier = 2.0
            
        # Calcula pontos com multiplicador
        points = int(base_points * self.multiplier)
        self.score += points
        
        # Atualiza high score se necessário
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        return points
    
    def take_damage(self, damage):
        if not self.is_alive:
            return
            
        self.current_health = max(0, self.current_health - damage)
        if self.current_health <= 0:
            self.game_over = True
            self.is_alive = False
    
    def heal(self, amount):
        if not self.is_alive:
            return
            
        self.current_health = min(self.max_health, self.current_health + amount)
    
    def reset(self):
        self.score = 0
        self.multiplier = 1.0
        self.current_health = self.max_health
        self.is_alive = True
        self.game_over = False
        self.level = 1
    
    def load_high_score(self):
        try:
            if os.path.exists('highscore.json'):
                with open('highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception as e:
            print(f"Error loading high score: {e}")
        return 0
    
    def save_high_score(self):
        try:
            with open('highscore.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception as e:
            print(f"Error saving high score: {e}")