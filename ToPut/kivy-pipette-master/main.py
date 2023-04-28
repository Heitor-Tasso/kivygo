from kivymd.app import MDApp

from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.graphics import *
from kivy.uix.label import Label

from behaviour.touch_behaviour import TouchBehavior

import os
from io import BytesIO
from PIL import Image as PILImage


class BorderImage(Image):
    border_ = BooleanProperty(False)


class TouchableScreen(Screen, TouchBehavior):
    pass


class PipetteMouse(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = Image(source='transparent.png', size_hint=(None, None), size=[64, 64])
        self.scaled_area = BorderImage(source='transparent.png', size_hint=(None, None), size=[90, 90])
        self.label_color = Label(size_hint=(None, None), color=(0.84, 0.78, 0.31, 1))

        self.add_widget(self.scaled_area)
        self.add_widget(self.cursor)
        self.add_widget(self.label_color)

    def set_cursor_icon(self, source: str):
        self.cursor.source = source
        self.cursor.reload()


class PipetteApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'pipette.png'
        self.screen = Builder.load_file('main.kv')

        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_keyboard=self.keyboard_handler)

        self.screen.bind(on_long_touch=self.on_long_touch)
        self.screen.bind(on_touch_up=self.on_touch_up)
        self.screen.bind(on_touch_move=self.touch_move)

        self.mouse = PipetteMouse()
        self.screen.add_widget(self.mouse)

        self.transparent_bg = 'transparent.png'

    def build(self):
        return self.screen

    def on_long_touch(self, inst, touch):
        if self.screen.ids.scr_manager.current != 'home':
            self.get_pixel(*touch.pos)
            self.mouse.scaled_area.border_ = True

    def on_touch_up(self, inst, touch):
        self.mouse.scaled_area.source = 'transparent.png'
        self.mouse.scaled_area.reload()
        self.mouse.scaled_area.border_ = False
        self.mouse.label_color.text = ''

    def show_cursor(self, show: bool):
        Window.show_cursor = show

    def touch_move(self, inst, touch):
        self.get_pixel(*touch.pos)

    def mouse_pos(self, window: Window, pos: tuple):
        self.mouse.cursor.pos = pos[0] - self.mouse.cursor.width // 2, pos[1] - self.mouse.cursor.height // 2

        self.mouse.scaled_area.pos = pos[0] - self.mouse.scaled_area.width // 2, pos[
            1] - self.mouse.scaled_area.height // 2

        self.mouse.label_color.pos = pos[0] - 50, pos[1] - 25

    def increasing_the_area(self, img: PILImage, pos: tuple):
        box_size = 50

        left = pos[0] - box_size / 2
        upper = pos[1] - box_size / 2

        right = left + box_size
        lower = upper + box_size

        """
        left - upper##############
        ##########################
        ##########################
        ##########################
        ##########################
        ##########################
        ###############right-lower
        """

        img = img.crop((left, upper, right, lower))
        img = img.resize((box_size * 4, box_size * 4), PILImage.ANTIALIAS)
        img = img.convert('RGB')

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        im = CoreImage(BytesIO(img_byte_arr), ext='png')

        self.mouse.scaled_area.texture = im.texture

    def get_widget_fbo(self, widget):
        scale = 1

        if widget.parent is not None:
            canvas_parent_index = widget.parent.canvas.indexof(widget.canvas)
            if canvas_parent_index > -1:
                widget.parent.canvas.remove(widget.canvas)

        fbo = Fbo(size=(widget.width * scale, widget.height * scale),
                  with_stencilbuffer=True
                  )

        with fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()
            Scale(1, -1, 1)
            Scale(scale, scale, 1)
            Translate(-widget.x, -widget.y - widget.height, 0)

        fbo.add(widget.canvas)
        fbo.draw()

        pil_img = PILImage.frombytes("RGBA", fbo.size, fbo.pixels).convert('RGB')

        fbo.remove(widget.canvas)

        if widget.parent is not None and canvas_parent_index > -1:
            widget.parent.canvas.insert(canvas_parent_index, widget.canvas)

        return pil_img

    def get_pixel(self, x: float, y: float):

        if self.screen.ids.scr_manager.current == '1':
            img = self.get_widget_fbo(self.screen.ids.layout_1)
        elif self.screen.ids.scr_manager.current == '2':
            img = self.get_widget_fbo(self.screen.ids.layout_2)
        else:
            return

        coords = int(x), img.height - int(y)

        try:
            color = img.getpixel(coords)

            self.increasing_the_area(img, coords)
            self.mouse.label_color.text = str(color)
            print('Area color:', color)
        except IndexError:
            color = ()

        return color

    def change_screen(self, name: str):
        if self.screen.ids.scr_manager.current != name:
            if name == 'home':
                self.screen.ids.scr_manager.transition.direction = 'right'
            else:
                self.screen.ids.scr_manager.transition.direction = 'left'

            self.screen.ids.scr_manager.current = name

    def keyboard_handler(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            self.change_screen('home')
            return True


PipetteApp().run()
