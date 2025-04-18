import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, PLAYER_SHOOT_COOLDOWN
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):       
        if self.cooldown > 0:
            return
        self.cooldown = PLAYER_SHOOT_COOLDOWN

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        return shot

    def update(self, dt):
        self.cooldown -= dt
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            # Rotate left
            self.rotate(-dt)
        if keys[pygame.K_e]:
            # Rotate right
            self.rotate(dt)
        if keys[pygame.K_COMMA]:
            # Move forward
            self.move(dt)
        if keys[pygame.K_o]:
            # Move backward
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            # Shoot
            shot = self.shoot()