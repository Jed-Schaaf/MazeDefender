# utils.py

# Constants
class Constants:
    """constants for the game"""
    TILE_SIZE = 32
    FPS = 30
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

# Colors
class Colors:
    """colors defined for the game"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    LIGHT_YELLOW = (255, 255, 160)
    PURPLE = (128, 0, 128)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    LIGHT_BLUE = (173, 216, 230)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, grid):
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        open_set.remove(current)
        x, y = current
        for dx, dy, dir_ in [(-1, 0, 'W'), (1, 0, 'E'), (0, -1, 'N'), (0, 1, 'S')]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and 
                dir_ in grid[y][x]):
                neighbor = (nx, ny)
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    open_set.add(neighbor)
    return []
