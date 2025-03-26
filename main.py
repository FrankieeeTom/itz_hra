from pyray import *
from raylib import *

WIN_WIDTH = 2000
WIN_HEIGHT = 1000

BACKGROUND_VEL = 100
ROAD_VEL = 500

GRAVITY = 500
JUMP_VEL = -500

class Scene:
    def __init__(self, velocity, position, texture):
        self.velocity = velocity
        self.position = position
        self.texture = texture
        self.offset = 0

    def draw(self, frame_time):

        self.offset = (self.offset + (self.velocity.x * frame_time)) % self.texture.width

        draw_texture_pro(
            self.texture,
            Rectangle(self.offset, 0, WIN_WIDTH, self.texture.height),
            Rectangle(self.position.x, self.position.y, WIN_WIDTH, self.texture.height),
            Vector2(0, 0),
            0,
            WHITE
        )

set_config_flags(FLAG_VSYNC_HINT)
init_window(WIN_WIDTH, WIN_HEIGHT, "Dino")
set_target_fps(30)
#set_window_state(FLAG_FULLSCREEN_MODE)

background_texture = load_texture("landscape.jpg")
road_texture = load_texture("road_ref2.jpg")

player_left_texture = load_texture("player_left_ref.png")
player_right_texture = load_texture("player_right_ref.png")
player_idle_texture = load_texture("player_idle_ref.png")

background = Scene(Vector2(BACKGROUND_VEL, 0), Vector2(0, 0), background_texture)

road = Scene(Vector2(ROAD_VEL, 0), Vector2(0, 750), road_texture)



player = Vector2(950, 1000)  # Player position
player_vel = 0  # Player velocity (initially at rest)
player_acc = 0  # Player acceleration (gravity)
is_jumping = False


player = {
    "x": 850,
    "y": 525,
    "texture": player_idle_texture
}


# main game loop
while not window_should_close():
    
    frame_time = get_frame_time()

    if is_key_pressed(KEY_F11):
        toggle_fullscreen()


    # backgorund, road and objects movement
    if is_key_down(KEY_RIGHT):
        background.velocity.x = BACKGROUND_VEL
        road.velocity.x = ROAD_VEL
        player["texture"] = player_right_texture

    elif is_key_down(KEY_LEFT):
        background.velocity.x = - BACKGROUND_VEL
        road.velocity.x = - ROAD_VEL
        player["texture"] = player_left_texture
    else:
        # If no keys are pressed, stop the background from moving
        background.velocity.x = 0
        road.velocity.x = 0
        player["texture"] = player_idle_texture

    # Jump logic
    if is_key_pressed(KEY_UP) and player["y"] == 525:  # Allow jump only if player is on the ground
        player_vel = JUMP_VEL
        is_jumping = True

    if is_jumping:
        # Apply gravity to player velocity
        player_vel += GRAVITY * frame_time
        player["y"] += player_vel * frame_time

    # Prevent player from going below the ground
    if player["y"] >= 525:
        player["y"] = 525
        player_vel = 0
        is_jumping = False

    # Start drawing
    begin_drawing()
    clear_background(WHITE)
    draw_fps(10, 10)
    
    # Draw the moving background and clouds
    background.draw(frame_time)
    road.draw(frame_time)

    # Draw the player
    draw_texture(player["texture"], int(player["x"]), int(player["y"]), WHITE)

    print(player["y"])
    
    end_drawing()

# Clean up and close
unload_texture(background_texture)
unload_texture(road_texture)
close_window()
