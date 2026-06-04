import arcade
import math

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAP = [
    "########........",
    "#......#........",
    "#...............",
    "#....##.........",
    "#......#........",
    "#......#........",
    "########........",
]

TILE = 50


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

    def cast_ray(self, angle):

        ray_x = self.player_x
        ray_y = self.player_y

        step = 4
        distance = 0

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        while distance < 1000:

            ray_x += cos_a * step
            ray_y += sin_a * step

            distance += step

            if self.is_wall(ray_x, ray_y):
                return distance

        return 1000

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

            distance = self.cast_ray(ray_angle)

            distance *= math.cos(
                ray_angle - self.player_angle
            )

            if distance < 1:
                distance = 1

            wall_height = (
                TILE * SCREEN_HEIGHT
            ) / distance

            brightness = max(
                30,
                min(
                    255,
                    int(255 - distance * 0.35)
                )
            )

            color = (
                brightness,
                brightness,
                brightness
            )

            x = ray * strip_width

            arcade.draw_rect_filled(
                arcade.LBWH(
                    x,
                    SCREEN_HEIGHT / 2
                    - wall_height / 2,
                    strip_width + 1,
                    wall_height
                ),
                color
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
            new_x += strafe_x * speed
            new_y += strafe_y * speed

        if self.move_right:
            new_x -= strafe_x * speed
            new_y -= strafe_y * speed

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

    def on_mouse_motion(
        self,
        x,
        y,
        dx,
        dy
    ):
        self.player_angle -= dx * 0.003
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