# MazeDefender

This game and readme were written using the Grok AI with light manual editing.

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
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Note: If a `requirements.txt` file is not present, ensure you have Pygame installed:
   ```bash
   pip install pygame
   ```

## Usage

To start the game, run the main script:
```bash
python main.py
```
Upon launching, you will be presented with a menu where you can adjust initial game parameters such as maze size, number of spawn points, waves, and enemies per wave. Use the arrow keys to navigate and modify these settings, then press Enter to begin the game.

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