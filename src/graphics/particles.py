# src/graphics/particles.py
import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color, velocity=(0, 0), lifetime=30, size=3, particle_type="normal"):
        self.x = x
        self.y = y
        self.original_color = color
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.original_lifetime = lifetime
        self.size = size
        self.type = particle_type
        self.alpha = 255
    
    def update(self):
        # Atualiza posição
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
        # Reduz tempo de vida
        self.lifetime -= 1
        
        # Atualiza alpha para fade out
        self.alpha = int((self.lifetime / self.original_lifetime) * 255)
        
        # Efeitos específicos por tipo
        if self.type == "fire":
            # Partículas de fogo ficam menores com o tempo
            self.size = max(1, self.size * 0.95)
            # Afeta velocidade para movimento mais orgânico
            self.velocity = (
                self.velocity[0] * 0.98,
                self.velocity[1] * 0.98 - 0.1
            )
        elif self.type == "spark":
            # Faíscas são afetadas pela gravidade
            self.velocity = (
                self.velocity[0] * 0.98,
                self.velocity[1] + 0.2
            )

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def create_explosion(self, x, y, color, particle_count=20):
        for _ in range(particle_count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            lifetime = random.randint(20, 40)
            size = random.randint(2, 4)
            
            particle = Particle(x, y, color, velocity, lifetime, size, "normal")
            self.particles.append(particle)
    
    def create_engine_fire(self, x, y):
        color = (255, random.randint(100, 200), 0)  # Tons de laranja
        velocity = (
            random.uniform(-0.5, 0.5),
            random.uniform(1, 3)
        )
        lifetime = random.randint(10, 20)
        size = random.randint(2, 4)
        
        particle = Particle(x, y, color, velocity, lifetime, size, "fire")
        self.particles.append(particle)
    
    def create_hit_sparks(self, x, y):
        for _ in range(5):
            color = (255, random.randint(200, 255), random.randint(0, 100))
            angle = random.uniform(-math.pi/4, math.pi/4)
            speed = random.uniform(3, 6)
            velocity = (
                math.cos(angle) * speed,
                -math.sin(angle) * speed
            )
            lifetime = random.randint(15, 25)
            size = random.randint(1, 3)
            
            particle = Particle(x, y, color, velocity, lifetime, size, "spark")
            self.particles.append(particle)
    
    def update(self):
        # Remove partículas mortas e atualiza as restantes
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
    
    def draw(self, surface):
        for particle in self.particles:
            # Cria superfície para partícula com alpha
            particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
            
            # Ajusta cor com alpha atual
            color_with_alpha = (*particle.color, particle.alpha)
            
            # Desenha partícula
            pygame.draw.circle(
                particle_surface,
                color_with_alpha,
                (particle.size, particle.size),
                particle.size
            )
            
            # Desenha na superfície principal
            surface.blit(
                particle_surface,
                (int(particle.x - particle.size), int(particle.y - particle.size))
            )