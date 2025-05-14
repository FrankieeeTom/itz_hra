from pyray import *
from raylib import *
from time import *

WIN_WIDTH = 2000
WIN_HEIGHT = 1000

BACKGROUND_VEL = 100
ROAD_VEL = 500

GRAVITY = 500
JUMP_VEL = -500
LEVEL_POS = 0

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

class Collision:
    def __init__(self, velocity, position, texture, width=300, height=30):
        self.velocity = velocity
        self.position = position
        self.texture = texture
        self.width = width
        self.height = height

    def update(self, frame_time):
        self.position.x -= self.velocity.x * frame_time

    def draw(self):
        draw_texture_pro(
            self.texture,
            Rectangle(0, 0, self.width, self.height),
            Rectangle(self.position.x, self.position.y, self.width, self.height),
            Vector2(0, 0),
            0,
            WHITE
        )

    def get_rect(self):
        return Rectangle(self.position.x, self.position.y, self.width, self.height)


player_right_idle = load_texture("textures/player_right_idle")
player_right_frame1 = load_texture("ref_textures/player_right_1_ref")
player_right_frame2 = load_texture("ref_textures/player_right_2_ref")
player_right_frame3 = load_texture("ref_textures/player_right_3_ref")


# Init
set_config_flags(FLAG_VSYNC_HINT)
init_window(WIN_WIDTH, WIN_HEIGHT, "Dino")
set_target_fps(60)

background_texture = load_texture("ref_textures/landscape.jpg")
road_texture = load_texture("ref_textures/road_ref2.jpg")
collision_texture = load_texture("ref_textures/kolize.png")
collision2_texture = load_texture("ref_textures/kolize2.png")

player_left_texture = load_texture("ref_textures/player_left_ref.png")
player_right_texture = load_texture("textures/player_right_1.png")
player_idle_texture = load_texture("textures/player_right_idle.png")

background = Scene(Vector2(BACKGROUND_VEL, 0), Vector2(0, 0), background_texture)
road = Scene(Vector2(ROAD_VEL, 0), Vector2(0, 750), road_texture)

platforms = [
    Collision(Vector2(ROAD_VEL, 0), Vector2(600, 600), collision_texture),
    Collision(Vector2(ROAD_VEL, 0), Vector2(1200, 400), collision_texture),
    Collision(Vector2(ROAD_VEL, 0), Vector2(1700, 500), collision_texture),
    Collision(Vector2(ROAD_VEL, 0), Vector2(2300, 325), collision_texture),
    Collision(Vector2(ROAD_VEL, 0), Vector2(2700, 450), collision_texture),
]

player = {
    "x": 850,
    "y": 525,
    "width": 100,
    "height": 215,
    "texture": player_idle_texture
}

player_vel = 0
is_jumping = False

player_frame_delay = 0

frame_delay = 0.5
last_frame_time = time()


current_frame = 0

# Main loop
while not window_should_close():
    frame_time = get_frame_time()

    if is_key_pressed(KEY_F11):
        toggle_fullscreen()

    # Hlavní logika LEVEL_POS
    if LEVEL_POS >= 0:
        if is_key_down(KEY_RIGHT):
            background.velocity.x = BACKGROUND_VEL
            road.velocity.x = ROAD_VEL
            for p in platforms:
                p.velocity.x = ROAD_VEL

            player["texture"] = player_right_texture 
            current_frame = 1
            LEVEL_POS += 5

        elif is_key_down(KEY_LEFT):
            background.velocity.x = -BACKGROUND_VEL
            road.velocity.x = -ROAD_VEL
            for p in platforms:
                p.velocity.x = -ROAD_VEL

            player["texture"] = player_left_texture
            LEVEL_POS -= 5

        else:
            background.velocity.x = 0
            road.velocity.x = 0
            for p in platforms:
                p.velocity.x = 0

            player["texture"] = player_idle_texture

    if LEVEL_POS <= 0:
        if LEVEL_POS <= -150:
            player["texture"] = player_idle_texture
            LEVEL_POS = -150
            player["x"] = 50

        road.velocity.x = 0
        background.velocity.x = 0
        for p in platforms:
            p.velocity.x = 0

        if is_key_down(KEY_RIGHT):
            player["x"] += 25
            player["texture"] = player_right_texture
            LEVEL_POS += 5

        elif is_key_down(KEY_LEFT):
            player["x"] -= 25
            player["texture"] = player_left_texture
            LEVEL_POS -= 5

        else:
            player["texture"] = player_idle_texture


    # Platform movement
    for p in platforms:
        p.update(frame_time)

    # Animace (volitelná)
    if not is_key_down(KEY_LEFT) and not is_key_down(KEY_RIGHT):
        if get_time() - last_frame_time >= frame_delay:
            current_frame = (current_frame + 1) % len(frames) if frames else 0
            last_frame_time = get_time()

    # Skok
    if is_key_pressed(KEY_UP) and not is_jumping:
        player_vel = JUMP_VEL
        is_jumping = True

    # Gravitace
    player_vel += GRAVITY * frame_time
    player["y"] += player_vel * frame_time

    # Kolize s plošinami
    player_rect = Rectangle(player["x"], player["y"], player["width"], player["height"])
    on_platform = False

    
    for plat in platforms:
        plat_rect = plat.get_rect()

        # Kontrola pouze pokud hráč padá
        if player_vel >= 0:
            # Hrany
            player_bottom = player["y"] + player["height"]
            platform_top = plat_rect.y

            # Horizontální překrytí
            if (player["x"] + player["width"] > plat_rect.x and player["x"] < plat_rect.x + plat_rect.width):

                # Je dostatečně blízko shora
                if abs(player_bottom - platform_top) <= 10:
                    player["y"] = platform_top - player["height"]
                    player_vel = 0
                    is_jumping = False
                    on_platform = True
                    break


    # Zem fallback
    if player["y"] >= 525 and not on_platform:
        player["y"] = 525
        player_vel = 0
        is_jumping = False

    # Kreslení
    begin_drawing()
    clear_background(WHITE)
    draw_fps(10, 10)


    background.draw(frame_time)
    road.draw(frame_time)

    for p in platforms:
        p.draw()

    
    texture = player["texture"]
    scale = 0.20  # Half size
    
    source_rec = Rectangle(0, 0, texture.width, texture.height)
    dest_rec = Rectangle(player["x"], player["y"], texture.width * scale, texture.height * scale)
    origin = Vector2(0, 0)
    rotation = 0.0

    draw_texture_pro(texture, source_rec, dest_rec, origin, rotation, WHITE)
 


    draw_text(str(LEVEL_POS), 20, 20, 65, WHITE)
    
    end_drawing()

# Cleanup
unload_texture(background_texture)
unload_texture(road_texture)
unload_texture(collision_texture)
unload_texture(player_left_texture)
unload_texture(player_right_texture)
unload_texture(player_idle_texture)
close_window()
