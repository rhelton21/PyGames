import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock

# Screen Dimensions
screenWidth = 600
screenHeight = 400

# Set Window Size
Window.size = (screenWidth, screenHeight)

# Gravity and upward movement rate
gravity = 0.05
upward_movement = -1.8

class Actor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = 50
        self.height = 30
        self.reset_position()

        self.dy = 0  # Initial Vertical Speed

        self.actor_image = CoreImage('assets/actor.gif').texture
        with self.canvas:
            self.rect = Rectangle(texture=self.actor_image, pos=(self.x, self.y), size=(self.width, self.height))

    def move(self):
        self.y -= self.dy  # self.y = self.y - self.dy
        self.rect.pos = (self.x, self.y)

    def reset_position(self):
        self.x = screenWidth / 2 - self.width / 2
        self.y = screenHeight / 2 - self.height / 2
        self.dy = 0
        if hasattr(self, 'rect'):
            self.rect.pos = (self.x, self.y)

class Obstacle(Widget):
    def __init__(self, gap, **kwargs):
        super().__init__(**kwargs)
        self.width = 30
        max_height = screenHeight - gap
        min_height = max(0, random.randint(self.width, max_height - self.width * 2))
        self.height_top = random.randint(min_height, max_height - self.width)
        self.height_bottom = max_height - self.height_top
        self.x = screenWidth
        self.y_top = screenHeight - self.height_top
        self.y_bottom = 0
        self.dx = -2  # Horizontal movement speed

        with self.canvas:
            self.rect_top = Rectangle(pos=(self.x, self.y_top), size=(self.width, self.height_top))
            self.rect_bottom = Rectangle(pos=(self.x, self.y_bottom), size=(self.width, self.height_bottom))

    def move(self):
        self.x += self.dx
        self.rect_top.pos = (self.x, self.y_top)
        self.rect_bottom.pos = (self.x, self.y_bottom)

class HelicopterGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Actor()
        self.add_widget(self.player)
        self.obstacles = []  # List to store obstacle widgets
        self.min_gap = self.player.height * 5

        # Add title and instruction Labels
        self.title = Label(text="HELICOPTER GAME", font_size="50sp", pos=(screenWidth / 2 - 50, screenHeight - 100))
        self.add_widget(self.title)

        self.instructions = Label(text="Press Spacebar to Play", font_size="25sp", pos=(screenWidth / 2 - 50, screenHeight / 2))
        self.add_widget(self.instructions)

        Window.bind(on_key_down=self.on_key_down)

        # Schedule the update method
        Clock.schedule_interval(self.update, 1 / 60)
        self.game_started = False  # Flag to check if the game has started

    def update(self, dt):
        if self.game_started:
            # Apply gravity to the helicopter
            self.player.dy += gravity
            self.player.move()

            # Generate Obstacles
            if random.random() < 0.02:  # Adjust this value for obstacle frequency
                obstacle_gap = random.randint(self.min_gap, screenHeight - self.min_gap)
                obstacle = Obstacle(gap=obstacle_gap)
                self.add_widget(obstacle)
                self.obstacles.append(obstacle)

            # Move and check collisions
            for obstacle in self.obstacles:
                obstacle.move()
                if obstacle.x < -obstacle.width:
                    self.remove_widget(obstacle)
                    self.obstacles.remove(obstacle)
                if self.check_collision(obstacle):
                    self.restart_game()

    def check_collision(self, obstacle):
        # Check collision with the top part of the obstacle
        if (self.player.x < obstacle.x + obstacle.width and self.player.x + self.player.width > obstacle.x and
                self.player.y < obstacle.y_top + obstacle.height_top and self.player.y + self.player.height > obstacle.y_top):
            return True
        # Check collision with the bottom part of the obstacle
        if (self.player.x < obstacle.x + obstacle.width and self.player.x + self.player.width > obstacle.x and
                self.player.y < obstacle.y_bottom + obstacle.height_bottom and self.player.y + self.player.height > obstacle.y_bottom):
            return True
        return False

    def restart_game(self):
        # Reset player position and speed
        self.player.reset_position()
        # Remove all obstacles
        for obstacle in self.obstacles:
            self.remove_widget(obstacle)
        self.obstacles.clear()
        # Reset game state
        self.game_started = False
        self.instructions.text = "Game Over : Press Spacebar to play again"
        self.add_widget(self.title)
        self.add_widget(self.instructions)

    def on_key_down(self, window, key, *args):
        if key == 32:  # Spacebar
            # Remove text labels and start the game when spacebar is pressed
            if not self.game_started:
                self.remove_widget(self.title)
                self.remove_widget(self.instructions)
                self.game_started = True

        elif key == 273 and self.game_started:  # Upward arrow key on the keyboard
            # Move the helicopter up when the upward arrow key is pressed
            self.player.dy = upward_movement

class HelicopterApp(App):
    def build(self):
        return HelicopterGame()

if __name__ == "__main__":
    HelicopterApp().run()
