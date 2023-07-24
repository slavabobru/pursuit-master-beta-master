from kivy.app import App
from kivy.uix.widget import Widget
import random
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.window import Keyboard
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


W,H = 700, 700
TILE = 45
GAME_RES = W * TILE, H * TILE

class GridGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.add_widget(
            BoxLayout())  # Добавление BoxLayout в качестве родительского виджета

        self.img = Image(
            source='res/player.png', pos = (60, 230))  # Замените на путь к вашему изображению

        self.add_widget(self.img)

        self.key_pressed = set()
        self.speed = 10

        self.update_event = Clock.schedule_interval(self.update, 1.0 / 60.0)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        self.key_codes = {
            Keyboard.keycodes['up']: 'up',
            Keyboard.keycodes['down']: 'down',
            Keyboard.keycodes['left']: 'left',
            Keyboard.keycodes['right']: 'right'
        }

    def update(self, dt):
        if 'up' in self.key_pressed:
            if self.img.y == 680:
                self.img.y -= 10
            else:
                self.img.y += self.speed
        if 'down' in self.key_pressed:
            if self.img.y == 210:
                self.img.y += 10
            else:
                self.img.y -= self.speed
        if 'left' in self.key_pressed:
            if self.img.x == 40:
                self.img.x += 10
            else:
                self.img.x -= self.speed
        if 'right' in self.key_pressed:
            if self.img.x == 870:
                self.img.x -= 10
            else:
                self.img.x += self.speed

    def on_key_down(self, window, key, *args):
        self.key_pressed.add(self.key_codes.get(key, ''))

    def on_key_up(self, window, key, *args):
        self.key_pressed.remove(self.key_codes.get(key, ''))

class Boss(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(BoxLayout())
        self.img = Image(source = "res/boss.png", pos = (870, 420))
        self.add_widget(self.img)
        self.velocity_x = 0
        self.velocity_y = 0

    def pursuit(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance < 50:
            self.velocity_x = dx / distance
            self.velocity_y = dy / distance
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.img.x == 870:
            self.img.x -= 10
        else:
            self.img.x += self.speed
        if self.img.x == 40:
            self.img.x += 10
        else:
            self.img.x -= self.speed
        if self.img.y == 210:
            self.img.y += 10
        else:
            self.img.y -= self.speed
        if self.img.y == 680:
            self.img.y -= 10
        else:
            self.img.y += self.speed

    def shoot(self):
        pass

class PursuitGame(Widget):
    my_grid = GridGame()
    my_boss = Boss()


class PursuitApp(App):
    def build(self):
        Window.bind(on_resize = self.on_window_resize)
        return PursuitGame()
    def on_start(self):
        self._width = self.root.ids["game_layout"].width
        self._height = self.root.ids["game_layout"].height
        self._width_glass = self._width / 20 * 12
        self._height_glass = self._height -40
        TILE_W = self._width_glass / W
        TILE_H = self._height_glass / H

    def on_window_resize(self, window, width, height):
        self._width = self.root.ids["game_layout"].width
        self._height = self.root.ids["game_layout"].height
        self._width_glass = self._width / 20 * 12
        self._height_glass = self._height - 40
        TILE_W = self._width_glass / W
        TILE_H = self._height_glass / H

        self.root.ids["game_layout_box"].canvas.clear()
        self.root.my_grid.download_player(self.root.ids["game_layout_box"], TILE_W, TILE_H)

if __name__ == "__main__":
    PursuitApp().run()

