# MazeDefender

This game and readme were written using the Grok AI with light manual editing.
You can read the full conversation [here](https://grok.com/share/c2hhcmQtMg%3D%3D_10b02b3f-241a-4bdc-9e6a-2ff4753c033e).

MazeDefender is a strategic maze-based game where players must navigate through a dynamically generated maze, collect resources, and defend their base from waves of enemies. The game features a unique blend of exploration, resource management, and tower defense mechanics. Players can build and upgrade towers to fend off enemies, collect pellets for resources, and utilize power-ups for temporary advantages. The game is built using Python and the Pygame library, offering a challenging and engaging experience for players.

## Installation

To play MazeDefender, you need to have Python installed on your system along with the Pygame library. Follow these steps to set up the game:

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/Jed-Schaaf/MazeDefender.git
   ```
2. Navigate to the project directory:
   ```bash
   cd MazeDefender
   ```
3. Ensure you have Pygame installed:
   ```bash
   pip install pygame
   ```

## Usage

To start the game, run the main script:
```bash
python main.py
```
Upon launching, you will be presented with a menu where you can adjust initial game parameters such as maze size, number of spawn points, waves, and enemies per wave. Use the arrow keys to navigate and modify these settings, then press Enter to begin the game.

### Menu Items
- **Width**: The number of horizontal tiles for the maze (range: 10-25; default: 20)
- **Height**: The number of vertical tiles for the maze (range: 10-16; default: 15)
- **Spawns**: The number of enemy spawning points (range: 1-3)
- **Waves**: The number of enemy waves to release (0 = infinite waves)
- **Enemies**: The number of enemies that will spawn in the first wave (minimum: 2; default: 10)

### Controls
- **Arrow keys**: Move the player
- **Spacebar**: Build or upgrade towers (when standing on a valid tile)
- Collect pellets to gain resources
- Avoid or destroy enemies to protect the base

## Game Mechanics

MazeDefender combines elements of maze navigation and tower defense. The game generates a braided maze with one-way walls, adding complexity to navigation and strategy. Key mechanics include:

- **Maze Generation**: A procedural braided maze with one-way walls that affect movement.
- **Player Movement**: Smooth movement with direction-based animations.
- **Resource Collection**: Pellets regenerate slowly over time, providing resources for tower construction and upgrades.
- **Tower Defense**: Build and upgrade towers to attack enemies.
- **Enemy AI**: Enemies have different behaviors, including chasing the player, wandering randomly around the maze, or moving towards the base. Enemies have one-way wall interactions.
- **Power-Ups**: Temporary boosts like speed, invincibility, or enemy freeze.
- **HUD and UI**: Displays resources, score, enemies, waves, and tower costs.

- If the player collides with an enemy, the base will not receive damage, but instead the player's speed will be reduced for a short time and the player will lose a certain percentage of resources. That enemy will also be destroyed.
- The number of enemies will increase by 2 with each successive wave. If the first wave has 10, then the second wave will have 12, the third 14, etc.
- Enemies gain hit points on successive waves, to be equal to the wave number.
- Enemies deal damage to the base equal to their current hit points.
- Upgrading a tower increases its damage to be equal to its level and increases attack rate by -0.5 seconds between attacks. The maximum level is 10, with 10 damage and 0.5 seconds between attacks.
- There is a 20-second delay at the beginning of each wave before enemies begin spawning, and a reducing delay per wave (down to a minimum) between individual enemies within a wave.

## Future Enhancements
- Add menu items for starting wave number, wave growth of number of enemies, and enemy strength increase per wave.
- Add a timer showing the remaining time before enemies spawn per wave.
- Add a current score display during gameplay in addition to the display at the end of a game.
- Adjust parameters, delays, and stats to achieve better balance and engagement.
- Change player-wall collision detection to use a circular player model instead of a rectangle for easier movement around the maze.
- Update the player's one-way wall collision to obey the one-way directions. (Partial entry into a one-way wall needs to be addressed.)

## Code Structure

The project is organized into several modules for clarity and maintainability:

- `main.py`: Handles the game loop, state management, and integration of components.
- `maze.py`: Generates the maze, including one-way walls and item placement.
- `player.py`: Manages player movement, interactions, and rendering.
- `enemy.py`: Controls enemy behavior, pathfinding, and rendering.
- `tower.py`: Implements tower mechanics, including upgrades and projectile firing.
- `ui.py`: Renders the user interface, including menus and HUD elements.
- `utils.py`: Provides utility functions and constants used across the project.

## Contributing

Contributions to MazeDefender are welcome! If you have ideas for new features, improvements, or bug fixes, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your changes.
3. Implement your changes, ensuring they align with the project's coding style.
4. Test your changes thoroughly.
5. Submit a pull request with a clear description of your modifications.

## License

MazeDefender is released under the GPL 3.0 License. See the `LICENSE` file in the repository for full details.

## Acknowledgements

- Developed by Jed Schaaf
- Built with Pygame: [Pygame Official Website](https://www.pygame.org/)
- Inspired by classic Pac-Man, maze, and tower defense games

---

This README provides a comprehensive overview of the MazeDefender project, ensuring that both players and developers can easily understand and engage with the game. For further details or to contribute, please visit the [GitHub repository](https://github.com/Jed-Schaaf/MazeDefender).
