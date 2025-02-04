import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

# Set the screen width and height
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Set the window size
Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 1, 0, 1)  # Add green color to the background
            Rectangle(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initial game state
        self.game_over = False

        # Initialize the game
        self.init_game()

        # Schedule the update function to move the snake
        Clock.schedule_interval(self.update, 1.0 / 10.0)

        # Bind keyboard events
        Window.bind(on_key_down=self.on_key_down)

    def init_game(self):
        # Create snake and food widgets
        self.snake = [Image(source='snake.bmp', size_hint=(None, None), size=(20, 20), pos=(100, 100))]
        self.food = Image(source='food.bmp', size_hint=(None, None), size=(20, 20))
        self.add_widget(self.snake[0])
        self.add_widget(self.food)

        # Initial snake movement direction
        self.direction = 'right'

        # Spawn food
        self.spawn_food()

        # Game over message
        self.game_over_label = Label(text="Game Over: Press Spacebar to play again", font_size='20sp',
                                     size_hint=(None, None), size=(SCREEN_WIDTH, 40),
                                     pos=(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2))
        self.game_over_label.opacity = 0  # Hide the label initially
        self.add_widget(self.game_over_label)

    def on_key_down(self, window, key, *args):
        if key == 32:  # Spacebar key
            if self.game_over:
                self.reset_game()
        elif not self.game_over:
            if key == 273 and self.direction != 'down':  # Up arrow key
                self.direction = 'up'
            elif key == 274 and self.direction != 'up':  # Down arrow key
                self.direction = 'down'
            elif key == 275 and self.direction != 'left':  # Right arrow key
                self.direction = 'right'
            elif key == 276 and self.direction != 'right':  # Left arrow key
                self.direction = 'left'

    def update(self, dt):
        if self.game_over:
            return

        # Move the snake
        x, y = self.snake[0].pos

        if self.direction == 'up':
            y += 20
        elif self.direction == 'down':
            y -= 20
        elif self.direction == 'right':
            x += 20
        elif self.direction == 'left':
            x -= 20

        # Check for collision with walls
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            self.end_game()
            return

        # Check for collision with itself
        for segment in self.snake[1:]:
            if self.snake[0].pos == segment.pos:
                self.end_game()
                return

        # Move the body segments
        prev_positions = [(segment.pos[0], segment.pos[1]) for segment in self.snake]
        self.snake[0].pos = (x, y)
        for i in range(1, len(self.snake)):
            self.snake[i].pos = prev_positions[i - 1]

        # Check for collision with food
        if self.check_collision(self.snake[0], self.food):
            self.grow_snake(prev_positions[-1])
            self.spawn_food()

    def check_collision(self, widget1, widget2):
        return widget1.collide_widget(widget2)

    def grow_snake(self, new_segment_pos):
        # Add a new segment to the snake at the position of the last segment
        new_segment = Image(source='snake.bmp', size_hint=(None, None), size=(20, 20), pos=new_segment_pos)
        self.snake.append(new_segment)
        self.add_widget(new_segment)

    def spawn_food(self):
        # Spawn the food at a random location
        food_x = random.randint(0, (SCREEN_WIDTH - 20) // 20) * 20
        food_y = random.randint(0, (SCREEN_HEIGHT - 20) // 20) * 20
        self.food.pos = (food_x, food_y)

    def end_game(self):
        # Set game over state
        self.game_over = True
        self.game_over_label.opacity = 1  # Show the game over label

        # Remove snake and food widgets
        for segment in self.snake:
            self.remove_widget(segment)
        self.remove_widget(self.food)

    def reset_game(self):
        # Reset game state
        self.game_over = False
        self.game_over_label.opacity = 0  # Hide the game over label

        # Reinitialize the game
        self.init_game()


class SnakeGameApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    SnakeGameApp().run()
