from raylib import *
from pyray import *
from config import *

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