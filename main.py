import arcade
import math
from arcade.types import Color

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAP = [
    "########........",
    "#......#........",
    "#...............",
    "#....###........",
    "#......#........",
    "#......#........",
    "########........",
]

TILE = 64


class Game(arcade.Window):

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            "Raycaster"
        )

        self.player_x = 100
        self.player_y = 100
        self.player_angle = 0

        self.move_forward = False
        self.move_back = False
        self.move_left = False
        self.move_right = False

        self.set_exclusive_mouse(True)
        self.wall_texture = arcade.load_texture("textures/wall.png")
        self.wall_texture_size = 64

    def is_wall(self, x, y):
        mx = int(x // TILE)
        my = int(y // TILE)

        if (
                mx < 0
                or my < 0
                or my >= len(MAP)
                or mx >= len(MAP[0])
        ):
            return True

        return MAP[my][mx] == "#"

    def cast_ray_dda(self, angle):
        ray_x = self.player_x
        ray_y = self.player_y
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        map_x = int(ray_x // TILE)
        map_y = int(ray_y // TILE)
        delta_dist_x = abs(1 / cos_a) if cos_a != 0 else 1e30
        delta_dist_y = abs(1 / sin_a) if sin_a != 0 else 1e30
        if cos_a < 0:
            step_x = -1
            side_dist_x = (ray_x - map_x * TILE) * delta_dist_x / TILE
        else:
            step_x = 1
            side_dist_x = ((map_x + 1) * TILE - ray_x) * delta_dist_x / TILE

        if sin_a < 0:
            step_y = -1
            side_dist_y = (ray_y - map_y * TILE) * delta_dist_y / TILE
        else:
            step_y = 1
            side_dist_y = ((map_y + 1) * TILE - ray_y) * delta_dist_y / TILE

        hit = False
        side = 0

        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            if map_x < 0 or map_y < 0 or map_y >= len(MAP) or map_x >= len(MAP[0]):
                hit = True
                break

            if MAP[map_y][map_x] == "#":
                hit = True
        if side == 0:
            distance = (side_dist_x - delta_dist_x) * TILE
        else:
            distance = (side_dist_y - delta_dist_y) * TILE
        if side == 0:
            wall_x = ray_y + distance * sin_a
        else:
            wall_x = ray_x + distance * cos_a

        wall_x %= TILE
        tex_x = int(wall_x)

        return distance, side, tex_x

    def on_draw(self):

        self.clear()

        arcade.draw_rect_filled(
            arcade.LBWH(
                0,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT // 2
            ),
            (70, 70, 70)
        )

        arcade.draw_rect_filled(
            arcade.LBWH(
                0,
                0,
                SCREEN_WIDTH,
                SCREEN_HEIGHT // 2
            ),
            (30, 30, 30)
        )

        fov = math.pi / 3
        num_rays = 400
        strip_width = SCREEN_WIDTH / num_rays

        for ray in range(num_rays):

            ray_angle = (
                    self.player_angle
                    - fov / 2
                    + ray * fov / num_rays
            )

            distance, side, tex_x = self.cast_ray_dda(ray_angle)

            if distance < 0.1:
                distance = 0.1

            wall_height = (
                                  TILE * SCREEN_HEIGHT
                          ) / distance

            base_brightness = max(30, min(255, int(255 - distance * 0.35)))
            if side == 1:
                base_brightness = int(base_brightness * 0.85)
            color = Color(base_brightness, base_brightness, base_brightness, 255)

            x = ray * strip_width
            y = SCREEN_HEIGHT / 2 - wall_height / 2
            arcade.draw_texture_rect(
                self.wall_texture,
                arcade.LBWH(
                    x,
                    y,
                    strip_width + 1,
                    wall_height
                ),
                color=color
            )

    def on_update(self, delta_time):

        speed = 250 * delta_time

        forward_x = math.cos(
            self.player_angle
        )

        forward_y = math.sin(
            self.player_angle
        )

        strafe_x = -forward_y
        strafe_y = forward_x

        new_x = self.player_x
        new_y = self.player_y

        if self.move_forward:
            new_x += forward_x * speed
            new_y += forward_y * speed

        if self.move_back:
            new_x -= forward_x * speed
            new_y -= forward_y * speed

        if self.move_left:
            new_x -= strafe_x * speed
            new_y -= strafe_y * speed

        if self.move_right:
            new_x += strafe_x * speed
            new_y += strafe_y * speed

        if not self.is_wall(
                new_x,
                self.player_y
        ):
            self.player_x = new_x

        if not self.is_wall(
                self.player_x,
                new_y
        ):
            self.player_y = new_y

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_angle += dx * 0.003
        self.player_angle %= math.tau

    def on_key_press(
            self,
            key,
            modifiers
    ):
        if key == arcade.key.W:
            self.move_forward = True

        elif key == arcade.key.S:
            self.move_back = True

        elif key == arcade.key.A:
            self.move_left = True

        elif key == arcade.key.D:
            self.move_right = True

    def on_key_release(
            self,
            key,
            modifiers
    ):
        if key == arcade.key.W:
            self.move_forward = False

        elif key == arcade.key.S:
            self.move_back = False

        elif key == arcade.key.A:
            self.move_left = False

        elif key == arcade.key.D:
            self.move_right = False


if __name__ == "__main__":
    Game()
    arcade.run()