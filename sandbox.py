from pyray import *
from raylib import *

class Scene:
    def __init__(self, width, height, texture):
        # Initialize window size and set up background image (optional)
        self.width = width
        self.height = height
        self.texture = texture
        self.background_x = 0  # Initial x position of the background
        self.background_y = 0  # Initial y position of the background
        self.bg_speed = 5  # Speed at which the background moves
        
        # Set up the window
        init_window(self.width, self.height, "Platformer Game")
        set_target_fps(60)  # Set the FPS limit

    def update(self):
        # Get key press states
        if is_key_pressed(KEY_RIGHT):
            self.background_x -= self.bg_speed  # Move background left when right arrow is pressed
        if is_key_pressed(KEY_LEFT):
            self.background_x += self.bg_speed  # Move background right when left arrow is pressed
        if is_key_pressed(KEY_DOWN):
            self.background_y -= self.bg_speed  # Move background up when down arrow is pressed
        if is_key_pressed(KEY_UP):
            self.background_y += self.bg_speed  # Move background down when up arrow is pressed

    def draw(self):
        # Draw the background (it will move based on background_x, background_y)
        clear_background(DARKGRAY)  # Clear the screen with a dark background color
        
        # Draw the moving background (for demonstration, we'll use a solid color background)
        draw_texture_pro(
            self.texture
            , Rectangle(self.offset, 0, self.width, self.texture.height)
            , Rectangle(self.position.x, self.position.y, self.width, self.texture.height)
            , Vector2(0, 0)
            , 0
            , WHITE
            
        )

        # You can add the player sprite here if you have one
        # draw_texture(player_texture, player_x, player_y)

    def run(self):
        # Main game loop
        while not window_should_close():
            self.update()  # Update background position based on input
            self.draw()  # Draw the updated scene

            # Update the window
            begin_drawing()

            # Clear the window and redraw everything
            self.draw()

            end_drawing()

        close_window()  # Close the window when done

# Create a new scene object and start the game loop
if __name__ == "__main__":
    scene = Scene(800, 600)
    scene.run()
