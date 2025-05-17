# enemy.py
import math
import pygame
import random
from utils import a_star, Colors, Constants

class Enemy:
    def __init__(self, spawn, behavior, maze, wave_number):
        self.pos = [spawn[0] * Constants.TILE_SIZE + 16, spawn[1] * Constants.TILE_SIZE + 16]
        self.behavior = behavior
        self.speed = 0.75 * Constants.TILE_SIZE / Constants.FPS
        self.path = []
        self.maze = maze
        self.target = None
        self.max_hit_points = wave_number
        self.hit_points = wave_number

    def update(self, player, game):
        if not self.path:
            start = (int(self.pos[0] / Constants.TILE_SIZE), int(self.pos[1] / Constants.TILE_SIZE))
            if self.behavior == 'shortest':
                self.target = self.maze.base
            elif self.behavior == 'chase':
                self.target = (int(player.pos[0] / Constants.TILE_SIZE), int(player.pos[1] / Constants.TILE_SIZE))
            else: #random_path
                if not self.target or start == self.target: #reached the random location
                    self.target = (random.randint(0, self.maze.width - 1), random.randint(0, self.maze.height - 1))
            self.path = a_star(start, self.target, self.maze.grid)

        if self.path and game.freeze_timer <= 0:
            next_pos = (self.path[0][0] * Constants.TILE_SIZE + 16, self.path[0][1] * Constants.TILE_SIZE + 16)
            dx = next_pos[0] - self.pos[0]
            dy = next_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.pos = list(next_pos)
                del self.path[0]
            else:
                angle = math.atan2(dy, dx)
                self.pos[0] += math.cos(angle) * self.speed
                self.pos[1] += math.sin(angle) * self.speed

        if math.hypot(self.pos[0] - self.maze.base[0] * Constants.TILE_SIZE - 16,
                      self.pos[1] - self.maze.base[1] * Constants.TILE_SIZE - 16) < 12:
            game.base_health -= 1
            game.score -= min(25, game.score)
            return True
        if math.hypot(self.pos[0] - player.pos[0], self.pos[1] - player.pos[1]) < 20:
            if player.invincible:
                game.score += 10
                return True
            elif player.resources > 0:
                player.resources = max(0, player.resources - max(1, player.resources // 4))
                game.score -= min(10, game.score)
                return True
            else:
                player.current_speed = player.current_speed * 0.75
        return False

    def draw(self, screen, time):
        cx = int(self.pos[0])
        cy = int(self.pos[1])
        arc_points = []
        for angle in range(180, 0, -18):
           rad = math.radians(angle)
           px = cx + 12 * math.cos(rad)
           py = cy + 12 * -math.sin(rad)
           arc_points.append((px, py))
        phase = time / 100.0
        wavy_points = []
        num_wavy = 10
        for i in range(num_wavy + 1):
           t = i / num_wavy
           x = cx + 12 - t * 24
           wave = 2 * math.sin(4 * math.pi * t + phase)
           y = cy + 12 + wave
           wavy_points.append((x, y))
        points = [(cx - 12, cy)] + arc_points + [(cx + 12, cy + 12)] + wavy_points + [(cx - 12, cy + 12), (cx - 12, cy)]
        pygame.draw.polygon(screen, Colors.RED, points)
        ratio = self.hit_points / self.max_hit_points
        color = Colors.GREEN if ratio > 0.5 else Colors.YELLOW if ratio > 0.25 else Colors.RED
        bar_width = int(24 * ratio)
        pygame.draw.rect(screen, color, (cx - 12, cy + 14, bar_width, 4))
        pygame.draw.rect(screen, Colors.BLACK, (cx - 12, cy + 14, 24, 4), 1)