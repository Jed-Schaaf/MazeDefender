# main.py
import asyncio
import platform
import pygame
import random
from maze import Maze
from player import Player
from enemy import Enemy
from ui import UI
from utils import Colors, Constants

pygame.init()
screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
pygame.display.set_caption("Maze Defender")
clock = pygame.time.Clock()

def draw_one_way_wall(screen, wall_type, x, y, direction, tile_size=Constants.TILE_SIZE):
    if wall_type == 'vertical':
        px = (x + 1) * tile_size
        py_top = y * tile_size
        py_bottom = (y + 1) * tile_size
        py_mid = (py_top + py_bottom) / 2
        if direction == 'east':
            pygame.draw.line(screen, Colors.DARK_GRAY, (px - 2, py_top), (px + 2, py_mid), 2)
            pygame.draw.line(screen, Colors.LIGHT_GRAY, (px - 2, py_bottom), (px + 2, py_mid), 2)
        else:  # 'west'
            pygame.draw.line(screen, Colors.LIGHT_GRAY, (px + 2, py_top), (px - 2, py_mid), 2)
            pygame.draw.line(screen, Colors.DARK_GRAY, (px + 2, py_bottom), (px - 2, py_mid), 2)
    elif wall_type == 'horizontal':
        py = (y + 1) * tile_size
        px_left = x * tile_size
        px_right = (x + 1) * tile_size
        px_mid = (px_left + px_right) / 2
        if direction == 'south':
            pygame.draw.line(screen, Colors.DARK_GRAY, (px_left, py - 2), (px_mid, py + 2), 2)
            pygame.draw.line(screen, Colors.LIGHT_GRAY, (px_right, py - 2), (px_mid, py + 2), 2)
        else:  # 'north'
            pygame.draw.line(screen, Colors.LIGHT_GRAY, (px_left, py + 2), (px_mid, py - 2), 2)
            pygame.draw.line(screen, Colors.DARK_GRAY, (px_right, py + 2), (px_mid, py - 2), 2)


class Game:
    def __init__(self):
        self.state = 'menu'
        self.menu_params = {'width': [20,{'min':10,'max':25}],
                            'height': [15,{'min':10,'max':16}],
                            'spawns': 2, 'waves': 5, 'enemies': 10}
        self.menu_select = 0
        self.maze = Maze(self.menu_params['width'][0], self.menu_params['height'][0], self.menu_params['spawns'])
        self.player = Player(self.maze)
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.base_health = 100
        self.score = 0
        self.wave_number = 0
        self.spawned_enemies = 0
        self.destroyed_enemies = 0
        self.total_enemies = 0
        self.wave_timer = 0
        self.spawn_timer = 0
        self.tower_boost_timer = 0
        self.freeze_timer = 0
        self.ui = UI(self)
        self.last_pellet_regen_time = 0
        self.last_powerup_regen_time = 0
        self.last_menu_arrow = 0

    def start_game(self):
        self.maze = Maze(self.menu_params['width'][0], self.menu_params['height'][0], self.menu_params['spawns'])
        global screen
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, self.maze.height * Constants.TILE_SIZE + 60))
        self.player = Player(self.maze)
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.base_health = 100
        self.score = 0
        self.wave_number = 1
        self.spawned_enemies = 0
        self.destroyed_enemies = 0
        self.total_enemies = self.menu_params['enemies']
        self.wave_timer = 20 * Constants.FPS
        self.state = 'playing'
        self.last_pellet_regen_time = pygame.time.get_ticks()
        self.last_powerup_regen_time = pygame.time.get_ticks()

    def draw(self, screen_, time):
        screen_.fill(Colors.BLACK)
        for wall in self.maze.wall_rects:
            pygame.draw.rect(screen_, Colors.WHITE, wall)
        for wall in self.maze.one_way_walls:
            draw_one_way_wall(screen_, *wall)
        for pellet in self.maze.pellets:
            pygame.draw.rect(screen_, Colors.YELLOW, (pellet[0] * Constants.TILE_SIZE + 14, pellet[1] * Constants.TILE_SIZE + 14, 4, 4))
        for powerup in self.maze.powerups:
            half_tile_size = Constants.TILE_SIZE // 2
            pygame.draw.circle(screen_, Colors.PURPLE, (powerup[0] * Constants.TILE_SIZE + half_tile_size, powerup[1] * Constants.TILE_SIZE + half_tile_size), 5)
        for spawn in self.maze.spawn_points:
            pygame.draw.rect(screen_, Colors.RED, (spawn[0] * Constants.TILE_SIZE + 1, spawn[1] * Constants.TILE_SIZE + 1, Constants.TILE_SIZE - 2, Constants.TILE_SIZE - 2))
        pygame.draw.rect(screen_, Colors.LIGHT_BLUE, (self.maze.base[0] * Constants.TILE_SIZE, self.maze.base[1] * Constants.TILE_SIZE, Constants.TILE_SIZE, Constants.TILE_SIZE))
        for tower in self.towers:
            tower.draw(screen_, time, self.tower_boost_timer)
        for enemy in self.enemies:
            enemy.draw(screen_, time)
        for proj in self.projectiles:
            proj.draw(screen_)
        self.player.draw(screen_, time)
        if self.state == 'menu':
            self.ui.draw_menu(screen_)
        elif self.state == 'playing':
            self.ui.draw_hud(screen_)
        elif self.state == 'game_over':
            self.ui.draw_game_over(screen_)

    def get_empty_cells(self):
        empty = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (x, y) not in self.maze.spawn_points and (x, y) != self.maze.base and \
                        (x, y) not in self.maze.pellets and (x, y) not in self.maze.powerups and \
                        not any(t.x == x and t.y == y for t in self.towers):
                    empty.append((x, y))
        return empty

    async def update(self):
        time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if self.state == 'menu':
            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                if time - self.last_menu_arrow >= 200:
                    if keys[pygame.K_UP]:
                        self.menu_select = (self.menu_select - 1) % len(self.menu_params)
                    elif keys[pygame.K_DOWN]:
                        self.menu_select = (self.menu_select + 1) % len(self.menu_params)
                    elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                        param = list(self.menu_params.keys())[self.menu_select]
                        delta = -1 if keys[pygame.K_LEFT] else 1
                        if param in ['width', 'height']:
                            self.menu_params[param][0] = max(self.menu_params[param][1]['min'], min(self.menu_params[param][1]['max'], self.menu_params[param][0] + delta))
                        elif param == 'spawns':
                            self.menu_params[param] = max(1, min(3, self.menu_params[param] + delta))
                        elif param == 'waves':
                            self.menu_params[param] = max(0, self.menu_params[param] + delta)
                        elif param == 'enemies':
                            self.menu_params[param] = max(2, self.menu_params[param] + delta)
                    self.last_menu_arrow = time
            elif keys[pygame.K_RETURN]:
                self.start_game()
            elif keys[pygame.K_q]:
                return False

        elif self.state == 'playing':
            if keys[pygame.K_ESCAPE]:
                self.state = 'game_over'
            else:
                self.player.update(keys, self, time)
                if self.wave_timer > 0:
                    self.wave_timer -= 1
                elif self.enemies or (self.menu_params['waves'] == 0 or self.wave_number <= self.menu_params['waves']):
                    spawn_rate = [4, 3, 2, 1, 0.5, 0.25][min(self.wave_number - 1, 5)] * Constants.FPS
                    self.spawn_timer -= 1
                    if self.spawn_timer <= 0 and self.spawned_enemies < self.total_enemies:
                        behavior = random.choice(['chase', 'shortest', 'random_path'])
                        spawn = random.choice(self.maze.spawn_points)
                        self.enemies.append(Enemy(spawn, behavior, self.maze, self.wave_number))
                        self.spawned_enemies += 1
                        self.spawn_timer = spawn_rate

                i = 0
                while i < len(self.enemies):
                    if self.enemies[i].update(self.player, self):
                        del self.enemies[i]
                        self.destroyed_enemies += 1
                    else:
                        i += 1

                for tower in self.towers:
                    proj = tower.update(self.enemies, self, time)
                    if proj:
                        self.projectiles.append(proj)

                i = 0
                while i < len(self.projectiles):
                    if self.projectiles[i].update(self.enemies, self):
                        del self.projectiles[i]
                    else:
                        i += 1

                if self.tower_boost_timer > 0:
                    self.tower_boost_timer -= 1
                if self.freeze_timer > 0:
                    self.freeze_timer -= 1

                if not self.enemies and self.spawned_enemies >= self.total_enemies and self.wave_timer <= 0:
                    self.wave_number += 1
                    self.score += 100
                    self.spawned_enemies = 0
                    self.destroyed_enemies = 0
                    self.total_enemies += 2
                    self.wave_timer = 20 * Constants.FPS

                if self.base_health <= 0 or (self.wave_number > self.menu_params['waves'] > 0):
                    self.state = 'game_over'

                current_time = pygame.time.get_ticks()
                if current_time - self.last_pellet_regen_time >= 10000:  # 10 seconds
                    empty_cells = self.get_empty_cells()
                    if empty_cells:
                        x, y = random.choice(empty_cells)
                        self.maze.pellets.append((x, y))
                        self.last_pellet_regen_time = current_time
                if current_time - self.last_powerup_regen_time >= 60000:  # 60 seconds
                    empty_cells = self.get_empty_cells()
                    if empty_cells:
                        x, y = random.choice(empty_cells)
                        self.maze.powerups.append((x, y))
                        self.last_powerup_regen_time = current_time

        elif self.state == 'game_over':
            if keys[pygame.K_m]:
                self.state = 'menu'
            elif keys[pygame.K_q]:
                return False

        self.draw(screen, time)
        pygame.display.flip()
        return True

async def main():
    game = Game()
    running = True
    while running:
        running = await game.update()
        await asyncio.sleep(1 / Constants.FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
