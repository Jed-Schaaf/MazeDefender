# ui.py
import pygame
from utils import Colors, Constants

class UI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)

    def draw_menu(self, screen):
        screen.fill(Colors.BLACK)
        game_title = self.font.render("Maze Defender", True, Colors.WHITE)
        screen.blit(game_title, (Constants.SCREEN_WIDTH // 2 - game_title.get_width() // 2, 10))
        for i, (param, val) in enumerate(self.game.menu_params.items()):
            color = Colors.YELLOW if i == self.game.menu_select else Colors.WHITE
            if param in ['width','height']:
                value = str(val[0]) + ' [' + str(val[1]['min']) + '..' + str(val[1]['max']) + ']'
            elif param == 'waves' and val == 0:
                value = 'infinite'
            elif param == 'spawns':
                value = str(val) + ' [1..3]'
            elif param == 'enemies':
                value = str(val) + ' (min: 2)'
            else:
                value = val
            text = self.font.render(f"{param}: {value}", True, color)
            screen.blit(text, (Constants.SCREEN_WIDTH // 2 - text.get_width() // 2, 60 + i * 30))
        instructions_y = 10 + game_title.get_height() + len(self.game.menu_params) * 30 + 60
        instructions1 = self.font.render("Use arrow keys to select and change parameters.", True, Colors.WHITE)
        instructions2 = self.font.render("Press Enter to start or Q to quit.", True, Colors.WHITE)
        instructions3 = self.font.render("In-game: move with arrow keys,", True, Colors.WHITE)
        instructions4 = self.font.render("build/upgrade towers with spacebar, end game with ESC.", True, Colors.WHITE)
        screen.blit(instructions1, (Constants.SCREEN_WIDTH // 2 - instructions1.get_width() // 2, instructions_y))
        screen.blit(instructions2, (Constants.SCREEN_WIDTH // 2 - instructions2.get_width() // 2, instructions_y + 30))
        screen.blit(instructions3, (Constants.SCREEN_WIDTH // 2 - instructions3.get_width() // 2, instructions_y + 60))
        screen.blit(instructions4, (Constants.SCREEN_WIDTH // 2 - instructions4.get_width() // 2, instructions_y + 90))

    def draw_hud(self, screen):
        y_pos = self.game.maze.height * Constants.TILE_SIZE + 5  # Position below maze
        resources_text = self.font.render(f"Resources: {self.game.player.resources}", True, Colors.WHITE)
        screen.blit(resources_text, (10, y_pos))
        center = (int(self.game.player.pos[0]) + 12, int(self.game.player.pos[1]) + 12)
        face = ({'right': center[0] + 12, 'left': center[0] - 12, 'up': center[0], 'down': center[0]}[self.game.player.direction],
                {'right': center[1], 'left': center[1], 'up': center[1] - 12, 'down': center[1] + 12}[self.game.player.direction])
        player_tile = (int(face[0] // Constants.TILE_SIZE),
                       int(face[1] // Constants.TILE_SIZE))
        if player_tile in self.game.maze.spawn_points or player_tile == self.game.maze.base:
            cost_str = "N/A"
            color = Colors.GRAY
            strikethrough = True
        else:
            tower = next((t for t in self.game.towers if t.x == player_tile[0] and t.y == player_tile[1]), None)
            if tower:
                if tower.level < 10:
                    cost = tower.level
                    cost_str = str(cost)
                else:
                    cost_str = "max"
                    cost = float('inf')
            else:
                cost = 5
                cost_str = str(cost)
            color = Colors.RED if self.game.player.resources < cost else Colors.WHITE
            strikethrough = False
        cost_text = self.font.render(f"Cost: {cost_str}", True, color)
        cost_pos = (10, y_pos + 30)
        screen.blit(cost_text, cost_pos)
        if strikethrough:
            pygame.draw.line(screen, color, (cost_pos[0], cost_pos[1] + cost_text.get_height() // 2),
                             (cost_pos[0] + cost_text.get_width(), cost_pos[1] + cost_text.get_height() // 2), 2)
        score_text = self.font.render(f"Score: {self.game.score}", True, Colors.WHITE)
        score_pos = (Constants.SCREEN_WIDTH // 2 - score_text.get_width() // 2, y_pos)
        screen.blit(score_text, score_pos)
        wave_text = self.font.render(f"Wave: {self.game.wave_number} / {self.game.menu_params['waves']}", True, Colors.WHITE)
        wave_pos = (Constants.SCREEN_WIDTH - 200, y_pos)
        screen.blit(wave_text, wave_pos)
        enemies_text = self.font.render(f"Enemies: {self.game.destroyed_enemies} / {self.game.total_enemies}", True, Colors.WHITE)
        enemies_pos = (Constants.SCREEN_WIDTH - 200, y_pos + 30)
        screen.blit(enemies_text, enemies_pos)

    def draw_game_over(self, screen):
        message = "You have won!" if self.game.wave_number > self.game.menu_params['waves'] else "You have lost."
        text1 = self.font.render(f"{message}", True, Colors.WHITE)
        text2 = self.font.render(f"Score: {self.game.score}", True, Colors.WHITE)
        width = max(text1.get_width(), text2.get_width()) + 40
        height = text1.get_height() * 2 + 30
        pygame.draw.rect(screen, Colors.DARK_GRAY,
                         (Constants.SCREEN_WIDTH // 2 - width // 2,
                          Constants.SCREEN_HEIGHT // 2 - height // 2, width, height))
        screen.blit(text1, (Constants.SCREEN_WIDTH // 2 - text1.get_width() // 2, Constants.SCREEN_HEIGHT // 2 - height // 2 + 10))
        screen.blit(text2, (Constants.SCREEN_WIDTH // 2 - text2.get_width() // 2, Constants.SCREEN_HEIGHT // 2 - height // 2 + 40))
        instructions = self.font.render("Press M to return to the menu or Q to quit", True, Colors.WHITE)
        pygame.draw.rect(screen, Colors.DARK_GRAY,
                         (Constants.SCREEN_WIDTH // 2 - instructions.get_width() // 2,
                          Constants.SCREEN_HEIGHT // 2 + instructions.get_height() * 2, instructions.get_width(), instructions.get_height()))
        screen.blit(instructions, (Constants.SCREEN_WIDTH // 2 - instructions.get_width() // 2, Constants.SCREEN_HEIGHT // 2 + 50))
