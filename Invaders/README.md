# Space Invaders Clone

A classic Space Invaders-style game built using Python and Pygame.

## 📜 Overview
This game is a modernized version of the classic arcade game **Space Invaders**, where the player controls a spaceship to shoot down waves of alien invaders.

## 🎮 Gameplay
- **Objective:** Destroy all aliens before they reach the bottom.
- **Controls:**
  - `←` and `→` (Arrow keys) - Move left and right.
  - `SPACE` - Shoot bullets.
  - `ESC` - Pause or exit the game.
- **Enemies:** Different types of alien invaders with unique abilities.
- **Lives:** The player starts with three lives; losing all results in game over.

## 🛠 Installation
### **Prerequisites**
Ensure you have Python and Pygame installed:
```sh
pip install pygame
```

### **Download and Run**
Clone the repository:
```sh
git clone https://github.com/yourusername/space-invaders.git
cd space-invaders
```
Run the game:
```sh
python SpaceInvaders.py
```

## 📂 Project Structure
```
Invaders/
│-- SpaceInvaders.py        # Main game script
│-- Game.py                 # Core game logic
│-- MainMenu.py             # Handles the main menu screen
│-- GamePlay.py             # Gameplay mechanics
│-- Alien.py                # Alien behavior and movement
│-- Player.py               # Player spaceship logic
│-- Laser.py                # Shooting mechanics
│-- images/                 # Sprites and assets
│-- fonts/                  # Custom fonts used in the game
```

## 🎨 Assets
- **Sprites:** Custom alien and player images.
- **Fonts:** Alien-themed fonts for UI elements.

## 🚀 Future Improvements
- Add power-ups.
- Implement different difficulty levels.
- Multiplayer mode.

## 🤝 Contributing
Feel free to fork the repository and submit pull requests!

## 📜 License
This project is open-source under the MIT License.
