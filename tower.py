# tower.py
import math
import pygame
from utils import Colors, Constants

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 1
        self.base_range = 3 * Constants.TILE_SIZE
        self.damage = 1
        self.fire_rate = 1
        self.last_shot = 0

    def get_time_between_shots(self):
        return max(1.0, 6.0 - (self.level - 1) * 0.5)

    def upgrade(self):
        self.level += 1
        self.damage = self.level

    def update(self, enemies, game, time):
        if time - self.last_shot < self.get_time_between_shots() * 1000:
            return None
        target, min_dist = None, float('inf')
        bx, by = game.maze.base
        range_ = self.base_range * (1.5 if game.tower_boost_timer > 0 else 1)
        half_tile_size = Constants.TILE_SIZE // 2
        for e in enemies:
            dist = math.hypot(e.pos[0] - (self.x * Constants.TILE_SIZE + half_tile_size),
                              e.pos[1] - (self.y * Constants.TILE_SIZE + half_tile_size))
            if dist <= range_:
                base_dist = math.hypot(e.pos[0] - (bx * Constants.TILE_SIZE + half_tile_size),
                              e.pos[1] - (by * Constants.TILE_SIZE + half_tile_size))
                if base_dist < min_dist:
                    min_dist = base_dist
                    target = e
        if target:
            self.last_shot = time
            return Projectile((self.x * Constants.TILE_SIZE + half_tile_size,
                               self.y * Constants.TILE_SIZE + half_tile_size), target, self.damage)
        return None

    def draw(self, screen, time, tower_boost_timer):
        size = 28
        offset = (Constants.TILE_SIZE - size) // 2
        pygame.draw.rect(screen, Colors.PURPLE, (self.x * Constants.TILE_SIZE + offset, self.y * Constants.TILE_SIZE + offset, size, size))
        pygame.draw.polygon(screen, Colors.GRAY, [(self.x * Constants.TILE_SIZE + offset + size / 2, self.y * Constants.TILE_SIZE + offset + size * 4 / 5),
                                           (self.x * Constants.TILE_SIZE + offset + size / 5, self.y * Constants.TILE_SIZE + size),
                                           (self.x * Constants.TILE_SIZE + offset + size * 4 / 5, self.y * Constants.TILE_SIZE + size)])
        center_point = self.y * Constants.TILE_SIZE + Constants.TILE_SIZE // 2
        individual_offset = self.y * 100 + self.x
        phase = math.sin(2 * math.pi * (time + individual_offset) / 1500)
        hover_offset = phase * 4
        gem_y = center_point + hover_offset
        pygame.draw.polygon(screen, Colors.LIGHT_GRAY, [(self.x * Constants.TILE_SIZE + 16, gem_y - 5),
                                                 (self.x * Constants.TILE_SIZE + 21, gem_y),
                                                 (self.x * Constants.TILE_SIZE + 16, gem_y + 5),
                                                 (self.x * Constants.TILE_SIZE + 11, gem_y)])
        pygame.draw.circle(screen, color=Colors.LIGHT_GRAY, width=1,
                           radius=self.base_range * (1.5 if tower_boost_timer > 0 else 1),
                           center=(self.x * Constants.TILE_SIZE + 16, self.y * Constants.TILE_SIZE + 16))
        level_text = pygame.font.Font(None, 20).render(str(self.level), True, Colors.WHITE)
        screen.blit(level_text, (self.x * Constants.TILE_SIZE + 24, self.y * Constants.TILE_SIZE + 24))
        ratio = min(1, (time - self.last_shot) / (self.get_time_between_shots() * 1000))
        pygame.draw.rect(screen, Colors.BLUE, (self.x * Constants.TILE_SIZE + 4, self.y * Constants.TILE_SIZE + 28, int(24 * ratio), 4))

class Projectile:
    def __init__(self, start, enemy, damage):
        self.pos = list(start)
        self.enemy = enemy
        self.speed = 5 * Constants.TILE_SIZE / Constants.FPS
        self.damage = damage

    def update(self, enemies, game):
        if self.enemy not in enemies:
            return True
        dx = self.enemy.pos[0] - self.pos[0]
        dy = self.enemy.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.enemy.hit_points -= self.damage
            if self.enemy.hit_points <= 0:
                enemies.remove(self.enemy)
                game.destroyed_enemies += 1
                game.score += 10
            return True
        angle = math.atan2(dy, dx)
        self.pos[0] += math.cos(angle) * self.speed
        self.pos[1] += math.sin(angle) * self.speed
        return False

    def draw(self, screen):
        dx = self.enemy.pos[0] - self.pos[0]
        dy = self.enemy.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist > 0:
            direction = (dx / dist, dy / dist)
            end_pos = (self.pos[0] + direction[0] * 10, self.pos[1] + direction[1] * 10)
            pygame.draw.line(screen, Colors.LIGHT_GRAY, (int(self.pos[0]), int(self.pos[1])),
                             (int(end_pos[0]), int(end_pos[1])), 2)
