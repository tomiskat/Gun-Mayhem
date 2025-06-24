# Gun Mayhem

A 2D action platformer developed in Python using Pygame, inspired by the popular browser game Gun Mayhem. Created
as a school project for Programming in Python course.


## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Gun-Mayhem
   ```

2. Create and activate a virtual environment:
   - **On Windows:**
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
   - **On Linux/macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python main.py
   ```

## 🎮 How to Play
  - **WASD/Arrow Keys**: Move player
  - **Space/P**: Shoot
  - **ESC**: Pause game

## 🏗️ Project Structure

```
Gun-Mayhem/
├── assets/            # Game assets (images, sounds, maps)
├── src/               
│   ├── constants/     # Game constants (colors, fonts)
│   ├── entities/      # Game entities (player, enemies)
│   ├── enums/         # Enumerations
│   ├── managers/      # Game and level managers
│   ├── model/         # Data models
│   ├── scenes/        # Game scenes (menu, level, pause)
│   ├── ui/            # User interface components
│   ├── utils/         # Utility functions
│   └── weapons/       # Weapon implementations
├── main.py            # Main game entry point
└── requirements.txt   # Python dependencies
```

## 🧩 Game Design

- **Game Scenes**:
  - `MenuScene`: Main menu with game options
  - `LevelScene`: Main gameplay area
  - `PauseScene`: Pause menu during gameplay

- **Entities**:
  - Player character with customizable controls
  - Various enemy typesy

- **Weapons**:
  - Base Weapon class for all weapons
  - Bullet physics and collision


## 🧪 Testing

The game was manually tested by playing through multiple levels and menus on various screen resolutions
and setups to ensure smooth gameplay and UI scaling. 

### Tested On:
- WQXGA (2560x1600)
- Full HD (1920x1080)

## 📸 Screenshots

### Main Menu
![Main Menu](assets/screenshots/menu.png)
### In-Game
![Gameplay](assets/screenshots/level.png)


