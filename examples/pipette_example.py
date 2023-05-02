import __init__
from kivygo.app import kivygoApp
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, NumericProperty
from kivy.graphics import ClearColor, ClearBuffers, Fbo, Scale, Translate
from kivy.uix.label import Label
from io import BytesIO
from PIL import Image as PILImage
from kivy.clock import Clock
from kivy.event import EventDispatcher


Builder.load_string("""

<BorderImage>
    canvas.after:
        Color:
            rgba: (0, 0, 0, 0.5) if root.border_ else (0, 0, 0, 0)
        Line:
            width: 1.2
            rectangle: (self.x, self.y, self.width, self.height)

        Color:
            rgba: (1, 1, 1, 0.5) if root.border_ else (0, 0, 0, 0)
        Line:
            width: 1.2
            rectangle: (self.x - 2.4, self.y - 2.4, self.width + 4.8, self.height + 4.8)


<TouchableScreen>:
    ScreenManager:
        id: scr_manager

        Screen:
            name: 'home'
            on_enter:
                app.mouse.set_cursor_icon('kivygo/icons/transparent.png')
                app.show_cursor(True)

            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(50)
                adaptive_size: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                Button:
                    text: 'Open demo with image'
                    on_release: app.change_screen('2')

        Screen:
            name: '2'
            on_enter:
                app.mouse.set_cursor_icon('kivygo/icons/pipette.png')
                app.show_cursor(False)
            BoxLayout:
                orientation: "vertical"
                Button:
                    size_hint_y: None
                    height: "40dp"
                    text: "LAST_SCREEN"
                    on_release: scr_manager.current = "home"
                Image:
                    id: layout_2
                    source: 'kivygo/images/test.jpg'


""")



class TouchBehavior(EventDispatcher):
    duration_long_touch = NumericProperty(0.4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_long_touch')
        self.bind(on_touch_down=self.create_clock, on_touch_up=self.delete_clock)
        self.clock = None

    def create_clock(self, widget, touch, *args):
        if self.collide_point(touch.x, touch.y):
            self.clock = Clock.schedule_once(lambda dt: self.clock_callback(touch), self.duration_long_touch)

    def delete_clock(self, widget, touch, *args):
        if self.collide_point(touch.x, touch.y):
            if self.clock:
                self.clock.cancel()

    def clock_callback(self, touch):
        self.dispatch('on_long_touch', touch)

    def on_long_touch(self, touch):
        pass


class BorderImage(Image):
    border_ = BooleanProperty(False)


class TouchableScreen(Screen, TouchBehavior):
    pass


class PipetteMouse(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = Image(source='kivygo/icons/transparent.png', size_hint=(None, None), size=[64, 64])
        self.scaled_area = BorderImage(source='kivygo/icons/transparent.png', size_hint=(None, None), size=[90, 90])
        self.label_color = Label(size_hint=(None, None), color=(0.84, 0.78, 0.31, 1))

        self.add_widget(self.scaled_area)
        self.add_widget(self.cursor)
        self.add_widget(self.label_color)

    def set_cursor_icon(self, source: str):
        self.cursor.source = source
        self.cursor.reload()


class PipetteApp(kivygoApp):

    def build(self):
        screen = TouchableScreen()

        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_keyboard=self.keyboard_handler)

        screen.bind(on_long_touch=self.on_long_touch)
        screen.bind(on_touch_up=self.on_touch_up)
        screen.bind(on_touch_move=self.touch_move)

        self.mouse = PipetteMouse()
        screen.add_widget(self.mouse)

        return screen

    def on_long_touch(self, inst, touch):
        if self.root.ids.scr_manager.current != 'home':
            self.get_pixel(*touch.pos)
            self.mouse.scaled_area.border_ = True

    def on_touch_up(self, inst, touch):
        self.mouse.scaled_area.source = 'kivygo/icons/transparent.png'
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

        if self.root.ids.scr_manager.current == '1':
            img = self.get_widget_fbo(self.root.ids.layout_1)
        elif self.root.ids.scr_manager.current == '2':
            img = self.get_widget_fbo(self.root.ids.layout_2)
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
        if self.root.ids.scr_manager.current != name:
            if name == 'home':
                self.root.ids.scr_manager.transition.direction = 'right'
            else:
                self.root.ids.scr_manager.transition.direction = 'left'

            self.root.ids.scr_manager.current = name

    def keyboard_handler(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            self.change_screen('home')
            return True


if __name__ == "__main__":
    PipetteApp().run()
