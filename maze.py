# maze.py
import random
import pygame
from utils import Constants

class Maze:
    def __init__(self, width, height, num_spawns):
        self.width = width
        self.height = height
        self.grid = [[set() for _ in range(width)] for _ in range(height)]
        self.generate_maze()
        self.remove_dead_ends()
        self.spawn_points = self.place_spawns(num_spawns)
        self.base = self.place_base()
        self.pellets = self.place_pellets()
        self.powerups = self.place_powerups()
        self.wall_rects = self.generate_wall_rects()
        self.one_way_walls = self.get_one_way_walls()

    def generate_maze(self):
        visited = set()
        stack = []

        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        visited.add((start_x, start_y))
        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            neighbors = [(nx, ny, d, o) for nx, ny, d, o in
                         [(x - 1, y, 'W', 'E'), (x + 1, y, 'E', 'W'), (x, y - 1, 'N', 'S'), (x, y + 1, 'S', 'N')]
                         if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited]
            if neighbors:
                nx, ny, dir_, opp = random.choice(neighbors)
                self.grid[y][x].add(dir_)
                self.grid[ny][nx].add(opp)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def remove_dead_ends(self):
        ONE_WAY_PROB = 0.3
        previous_dead_ends = set()
        while True:
            dead_ends = [(x, y) for y in range(self.height) for x in range(self.width) if len(self.grid[y][x]) == 1]
            if not dead_ends or set(dead_ends) == previous_dead_ends:
                break
            previous_dead_ends = set(dead_ends)
            for x, y in dead_ends:
                dirs = [(nx, ny, d, o) for nx, ny, d, o in
                        [(x - 1, y, 'W', 'E'), (x + 1, y, 'E', 'W'), (x, y - 1, 'N', 'S'), (x, y + 1, 'S', 'N')]
                        if 0 <= nx < self.width and 0 <= ny < self.height and d not in self.grid[y][x]]
                if dirs:
                    nx, ny, dir_, opp = random.choice(dirs)
                    if random.random() < ONE_WAY_PROB:
                        self.grid[y][x].add(dir_)  # One-way from (x,y) to (nx,ny)
                    else:
                        self.grid[y][x].add(dir_)
                        self.grid[ny][nx].add(opp)  # Two-way connection

    def place_spawns(self, num):
        return random.sample([(0, y) for y in range(self.height)], min(num, self.height))

    def place_base(self):
        return self.width - 1, random.randint(0, self.height - 1)

    def place_pellets(self):
        pellets = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in self.spawn_points and (x, y) != self.base and random.random() < 0.2:
                    pellets.append((x, y))
        return pellets

    def place_powerups(self):
        powerups = []
        for _ in range(5):
            while True:
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                if (x, y) not in self.spawn_points and (x, y) != self.base and (x, y) not in self.pellets:
                    powerups.append((x, y))
                    break
        return powerups

    def generate_wall_rects(self):
        walls = [
            pygame.Rect(0, 0, self.width * Constants.TILE_SIZE, 2),
            pygame.Rect(0, self.height * Constants.TILE_SIZE - 2, self.width * Constants.TILE_SIZE, 2),
            pygame.Rect(0, 0, 2, self.height * Constants.TILE_SIZE),
            pygame.Rect(self.width * Constants.TILE_SIZE - 2, 0, 2, self.height * Constants.TILE_SIZE)
        ]
        for y in range(self.height):
            for x in range(self.width - 1):
                if 'E' not in self.grid[y][x] and 'W' not in self.grid[y][x + 1]:
                    walls.append(pygame.Rect((x + 1) * Constants.TILE_SIZE - 1, y * Constants.TILE_SIZE, 2, Constants.TILE_SIZE))
        for y in range(self.height - 1):
            for x in range(self.width):
                if 'S' not in self.grid[y][x] and 'N' not in self.grid[y + 1][x]:
                    walls.append(pygame.Rect(x * Constants.TILE_SIZE, (y + 1) * Constants.TILE_SIZE - 1, Constants.TILE_SIZE, 2))
        return walls

    def get_one_way_walls(self):
        one_way_walls = []
        for y in range(self.height):
            for x in range(self.width - 1):
                if 'E' in self.grid[y][x] and 'W' not in self.grid[y][x + 1]:
                    one_way_walls.append(('vertical', x, y, 'east'))
                elif 'W' in self.grid[y][x + 1] and 'E' not in self.grid[y][x]:
                    one_way_walls.append(('vertical', x, y, 'west'))
        for y in range(self.height - 1):
            for x in range(self.width):
                if 'S' in self.grid[y][x] and 'N' not in self.grid[y + 1][x]:
                    one_way_walls.append(('horizontal', x, y, 'south'))
                elif 'N' in self.grid[y + 1][x] and 'S' not in self.grid[y][x]:
                    one_way_walls.append(('horizontal', x, y, 'north'))
        return one_way_walls
