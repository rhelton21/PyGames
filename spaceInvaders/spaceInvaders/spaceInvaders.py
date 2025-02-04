from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ListProperty, ObjectProperty
from random import randint

# Set the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the window size
Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)

class Bullet(Widget):
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)  # White color for the bullet
            self.rect = Rectangle(size=(5, 10), pos=self.pos)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Enemy(Image):  # Inherit from Image to use the enemy image
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.source = 'assets/enemies.png'  # Use the enemy image file
        self.size_hint = (None, None)
        self.size = (40, 40)  # Set the size of the enemy

class SpaceInvaderGame(Widget):
    bullets = ListProperty([])
    enemies = ListProperty([])
    game_over_image = ObjectProperty(None)
    game_over_flag = False

    def __init__(self, **kwargs):
        super(SpaceInvaderGame, self).__init__(**kwargs)
        with self.canvas:
            # Set background color
            Color(0, 0, 0, 1)  # Black color
            self.rect = Rectangle(size=(SCREEN_WIDTH, SCREEN_HEIGHT), pos=(0, 0))

        # Load and position the spaceship image
        self.spaceship = Image(source='assests/spaceship.png')
        self.spaceship.size_hint = (None, None)  # Disable size hint to use fixed size
        self.spaceship.size = (64, 64)  # Set the size of the spaceship
        self.spaceship.pos = (SCREEN_WIDTH / 2 - self.spaceship.width / 2, 0)  # Centered x, bottom y
        self.add_widget(self.spaceship)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.left_pressed = False
        self.right_pressed = False

        # Schedule updates
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.0)  # Check to spawn enemies every second

        # Initialize with a sufficient number of enemies
        self.init_enemies()

    def on_key_down(self, window, key, *args):
        if key == 276:  # Left arrow key
            self.left_pressed = True
        elif key == 275:  # Right arrow key
            self.right_pressed = True
        elif key == 32:  # Spacebar key
            self.fire_bullet()

    def on_key_up(self, window, key, *args):
        if key == 276:  # Left arrow key
            self.left_pressed = False
        elif key == 275:  # Right arrow key
            self.right_pressed = False

    def update(self, dt):
        if self.game_over_flag:
            return

        # Move spaceship based on key presses
        if self.left_pressed and self.spaceship.x > 0:
            self.spaceship.x -= 5
        if self.right_pressed and self.spaceship.right < SCREEN_WIDTH:
            self.spaceship.x += 5

        # Move bullets
        for bullet in self.bullets:
            bullet.y += 10
            if bullet.y > SCREEN_HEIGHT:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

        # Move enemies
        for enemy in self.enemies:
            enemy.y -= 2
            if enemy.y < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)

        # Check for collisions
        self.check_collisions()

    def fire_bullet(self):
        if self.game_over_flag:
            return

        bullet = Bullet()
        bullet.size = (5, 10)
        bullet.pos = (self.spaceship.center_x - bullet.width / 2, self.spaceship.top)
        self.add_widget(bullet)
        self.bullets.append(bullet)

    def spawn_enemy(self, dt):
        if self.game_over_flag:
            return

        # Ensure no fewer than 10 enemies and no more than 15 enemies
        while len(self.enemies) < 15:
            enemy = Enemy()
            enemy.pos = (randint(0, SCREEN_WIDTH - enemy.width), SCREEN_HEIGHT)
            self.add_widget(enemy)
            self.enemies.append(enemy)

    def init_enemies(self):
        # Initialize with a sufficient number of enemies
        for _ in range(10):  # Start with 10 enemies
            enemy = Enemy()
            enemy.pos = (randint(0, SCREEN_WIDTH - enemy.width), SCREEN_HEIGHT)
            self.add_widget(enemy)
            self.enemies.append(enemy)

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if self.is_collision(bullet, enemy):
                    self.remove_widget(bullet)
                    self.remove_widget(enemy)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

        for enemy in self.enemies[:]:
            if self.is_collision(enemy, self.spaceship):
                self.game_over()

    def is_collision(self, obj1, obj2):
        if (obj1.x < obj2.right and obj1.right > obj2.x and
            obj1.y < obj2.top and obj1.top > obj2.y):
            return True
        return False

    def game_over(self):
        self.game_over_flag = True

        # Remove all current widgets (bullets and enemies)
        for bullet in self.bullets:
            self.remove_widget(bullet)
        for enemy in self.enemies:
            self.remove_widget(enemy)

        # Clear lists
        self.bullets.clear()
        self.enemies.clear()

        # Display game over image
        self.game_over_image = Image(source='gameover.png')
        self.game_over_image.size_hint = (None, None)
        self.game_over_image.size = (400, 200)
        self.game_over_image.pos = (SCREEN_WIDTH / 2 - self.game_over_image.width / 2,
                                    SCREEN_HEIGHT / 2 - self.game_over_image.height / 2)
        self.add_widget(self.game_over_image)

class SpaceInvaderApp(App):
    def build(self):
        return SpaceInvaderGame()

if __name__ == '__main__':
    SpaceInvaderApp().run()
