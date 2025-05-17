# player.py
import pygame
import math
import random
from tower import Tower
from utils import Colors, Constants

class Player:
    def __init__(self, maze):
        self.maze = maze
        self.pos = self.pos = [ (self.maze.width // 2) * 32 + 4, (self.maze.height // 2) * 32 + 4 ]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 24, 24)
        self.speed = 2 * Constants.TILE_SIZE / Constants.FPS
        self.resources = 0
        self.direction = 'right'
        self.invincible = False
        self.invincibility_timer = 0
        self.speed_boost_timer = 0
        self.current_speed = self.speed
        self.moving = False
        self.last_build_time = 0

    def update(self, keys, game, time):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx, self.direction = -self.current_speed, 'left'
        elif keys[pygame.K_RIGHT]:
            dx, self.direction = self.current_speed, 'right'
        elif keys[pygame.K_UP]:
            dy, self.direction = -self.current_speed, 'up'
        elif keys[pygame.K_DOWN]:
            dy, self.direction = self.current_speed, 'down'

        self.moving = dx != 0 or dy != 0

        new_pos = [self.pos[0] + dx, self.pos[1] + dy]
        new_rect = pygame.Rect(new_pos[0], new_pos[1], 24, 24)
        if not any(new_rect.colliderect(wall) for wall in self.maze.wall_rects):
            self.pos = new_pos
            self.rect = new_rect

        if keys[pygame.K_SPACE] and time - self.last_build_time >= 500:
            x, y = int(self.pos[0] / Constants.TILE_SIZE), int(self.pos[1] / Constants.TILE_SIZE)
            tower = next((t for t in game.towers if t.x == x and t.y == y), None)
            if tower and tower.level < 10 and self.resources >= tower.level:
                self.resources -= tower.level
                tower.upgrade()
            elif (x, y) not in self.maze.spawn_points and (x, y) != self.maze.base and \
                    (x, y) not in self.maze.pellets and (x, y) not in self.maze.powerups and \
                    not tower and self.resources >= 5:
                game.towers.append(Tower(x, y))
                self.resources -= 5
            self.last_build_time = time

        for i, pellet in enumerate(self.maze.pellets):
            if self.rect.collidepoint(pellet[0] * Constants.TILE_SIZE + 16, pellet[1] * Constants.TILE_SIZE + 16):
                self.resources += 1
                game.score += 1
                del self.maze.pellets[i]
                break

        for i, powerup in enumerate(self.maze.powerups):
            if self.rect.collidepoint(powerup[0] * Constants.TILE_SIZE + 16, powerup[1] * Constants.TILE_SIZE + 16):
                effect = random.choice(['speed', 'invincibility', 'tower_boost', 'freeze'])
                if effect == 'speed':
                    self.speed_boost_timer = 10 * Constants.FPS
                    self.current_speed = self.speed * 1.5
                elif effect == 'invincibility':
                    self.invincible = True
                    self.invincibility_timer = 15 * Constants.FPS
                elif effect == 'tower_boost':
                    game.tower_boost_timer = 20 * Constants.FPS
                elif effect == 'freeze':
                    game.freeze_timer = 5 * Constants.FPS
                del self.maze.powerups[i]
                break

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.current_speed = self.speed

    def draw(self, screen, time):
        color = Colors.LIGHT_YELLOW if self.invincible and (time // 10) % 2 else Colors.YELLOW
        center = (int(self.pos[0]) + 12, int(self.pos[1]) + 12)
        radius = 12
        mouth_angle = 40 * abs(math.sin(time / 100)) if self.moving else 0
        start_angle = {'right': 0, 'left': 180, 'up': 90, 'down': 270}[self.direction]
        if mouth_angle == 0:
            pygame.draw.circle(screen, color, center, radius)
            face = ({'right': center[0]+12, 'left': center[0]-12, 'up': center[0], 'down': center[0]}[self.direction],
                    {'right': center[1], 'left': center[1], 'up': center[1]-12, 'down': center[1]+12}[self.direction])
            pygame.draw.line(screen, Colors.BLACK, center, face, 1)
        else:
            arc_points = []
            step = 5
            start_arc = (start_angle + mouth_angle) % 360
            end_arc = (start_angle - mouth_angle + 360) % 360
            num_points = int((360 - 2*mouth_angle) // step)
            for i in range(num_points):
                current_angle = i * step + start_arc
                rad = math.radians(current_angle)
                px = center[0] + radius * math.cos(rad)
                py = center[1] - radius * math.sin(rad)
                arc_points.append((px, py))
            rad = math.radians(end_arc)
            px = center[0] + radius * math.cos(rad)
            py = center[1] - radius * math.sin(rad)
            arc_points.append((px, py))
            points = [center] + arc_points
            pygame.draw.polygon(screen, color, points)
