import arcade
from pyglet.event import EVENT_HANDLE_STATE
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_NAME = 'тест'

MAP = [
    "########",
    "#.......",
    "#.......",
    "#.......",
    "#......#",
    "#......#",
    "########",
]

BLOCK = 50


class MainGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_NAME)

        self.player_x = 140
        self.player_y = 140
        self.player_angle = 0

        self.set_exclusive_mouse(True)

        self.forward_pressed = False
        self.backward_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        self.clear()
        for i, row in enumerate(MAP):
            for j, elem in enumerate(row):
                if elem == '#':
                    arcade.draw_lbwh_rectangle_filled(
                        j * BLOCK,
                        i * BLOCK,
                        BLOCK,
                        BLOCK,
                        (100, 100, 100)
                    )

        # игрок
        arcade.draw_lbwh_rectangle_filled(
            self.player_x,
            self.player_y,
            BLOCK / 2,
            BLOCK / 2,
            (250, 0, 0)
        )
        fov = math.pi / 3
        num_rays = 60

        for ray in range(num_rays):

            ray_angle = self.player_angle - fov / 2 + (ray / num_rays) * fov

            ray_x = self.player_x
            ray_y = self.player_y

            distance = 0

            while distance < 800:

                ray_x += math.cos(ray_angle)
                ray_y += math.sin(ray_angle)
                distance += 1

                map_x = int(ray_x // BLOCK)
                map_y = int(ray_y // BLOCK)

                if (
                        map_x < 0 or map_x >= len(MAP[0]) or
                        map_y < 0 or map_y >= len(MAP)
                ):
                    break

                if MAP[map_y][map_x] == "#":
                    break

            arcade.draw_line(
                self.player_x,
                self.player_y,
                ray_x,
                ray_y,
                arcade.color.YELLOW,
                1
            )

    def on_update(self, delta_time: float):

        move_speed = 200 * delta_time
        forward_x = math.cos(self.player_angle)
        forward_y = math.sin(self.player_angle)
        strafe_x = -forward_y
        strafe_y = forward_x

        if self.forward_pressed:
            self.player_x += forward_x * move_speed
            self.player_y += forward_y * move_speed

        if self.backward_pressed:
            self.player_x -= forward_x * move_speed
            self.player_y -= forward_y * move_speed

        if self.left_pressed:
            self.player_x += strafe_x * move_speed
            self.player_y += strafe_y * move_speed

        if self.right_pressed:
            self.player_x -= strafe_x * move_speed
            self.player_y -= strafe_y * move_speed

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.forward_pressed = True
        if key == arcade.key.S:
            self.backward_pressed = True
        if key == arcade.key.A:
            self.left_pressed = True
        if key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.forward_pressed = False
        if key == arcade.key.S:
            self.backward_pressed = False
        if key == arcade.key.A:
            self.left_pressed = False
        if key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> EVENT_HANDLE_STATE:
        self.player_angle += -dx * 0.002
        self.player_angle %= math.tau


if __name__ == "__main__":
    game = MainGame()
    game.run()