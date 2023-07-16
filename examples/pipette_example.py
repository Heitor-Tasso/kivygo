import __init__
from kivygo.app import GoApp
from kivygo.widgets.button import GoButtonRipple
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
from kivy.metrics import dp


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


<PipetteExample>:
    ScreenManager:
        id: scr_manager

        Screen:
            name: 'home'
            on_enter:
                root.mouse.set_cursor_icon('kivygo/icons/transparent.png')
                root.show_cursor(True)

            GoButtonRipple:
                text: 'Open demo with image'
                on_release: root.change_screen('2')

        Screen:
            name: '2'
            on_enter:
                root.mouse.set_cursor_icon('kivygo/icons/pipette.png')
                root.show_cursor(False)
            BoxLayout:
                orientation: "vertical"
                # Widget:
                GoButtonRipple:
                    size_hint_y: None
                    height: "40dp"
                    text: "LAST_SCREEN"
                    on_release: scr_manager.current = "home"
                # AnchorLayout:
                #     anchor_y: 'center'
                    # size_hint_y: None
                    # height: layout_2.height + dp(50)
                Image:
                    id: layout_2
                    source: 'kivygo/images/test.jpg'
                        # size_hint_y: None
                        # height: self.texture.size[1] * 0.25
                # Widget:

""")


class BorderImage(Image):
    border_ = BooleanProperty(False)


class PipetteExample(Screen):

    duration_long_touch = NumericProperty(0.4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_keyboard=self.keyboard_handler)
        self.can_draw = False
        self.clock = None
        self.register_event_type('on_long_touch')
        self.bind(
            on_touch_down=self.create_clock,
            on_touch_up=self.delete_clock
        )
        Clock.schedule_once(self.config)
    
    def config(self, *args):
        self.mouse = PipetteMouse()
        Window.add_widget(self.mouse)

    def create_clock(self, widget, touch, *args):
        self.can_draw = False
        if self.collide_point(*touch.pos):
            self.can_draw = True
            self.clock = Clock.schedule_once(
                lambda dt: self.clock_callback(touch),
                self.duration_long_touch
            )

    def delete_clock(self, widget, touch, *args):
        if self.collide_point(*touch.pos):
            if self.clock:
                self.clock.cancel()

    def clock_callback(self, touch):
        self.dispatch('on_long_touch', touch)

    def on_long_touch(self, touch, *args):
        if self.ids.scr_manager.current != 'home':
            self.get_pixel(*self.to_local(*touch.pos))
            self.mouse.scaled_area.border_ = True

    def on_touch_up(self, touch, *args):
        self.mouse.scaled_area.source = 'kivygo/icons/transparent.png'
        self.mouse.scaled_area.reload()
        self.mouse.scaled_area.border_ = False
        self.mouse.label_color.text = ''

    def show_cursor(self, show: bool):
        Window.show_cursor = show

    def on_touch_move(self, touch, *args):
        if not self.can_draw:
            return False
        
        self.get_pixel(*self.to_local(*touch.pos))

    def mouse_pos(self, win, pos):
        if not self.can_draw:
            return False
        
        x, y = tuple(map(lambda x: dp(x), pos))

        self.mouse.cursor.pos = [
            x - (self.mouse.cursor.width/2),
            y - (self.mouse.cursor.height/2)
        ]
        
        self.mouse.scaled_area.pos = [
            self.mouse.cursor.center_x - (self.mouse.scaled_area.width / 2),
            self.mouse.cursor.center_y - (self.mouse.scaled_area.height / 2)
        ]
        
        self.mouse.label_color.pos = [
            self.mouse.cursor.center_x - (self.mouse.label_color.width / 2),
            self.mouse.cursor.y - self.mouse.label_color.texture_size[1] - dp(10)
        ]

    def increasing_the_area(self, img, pos):
        box_size = dp(50)
        x, y = pos

        left = int(x - (box_size / 2))
        upper = int(y - (box_size / 2))

        right = int(left + box_size)
        lower = int(upper + box_size)

        img = img.crop((left, upper, right, lower))
        img = img.resize(
            ( int(box_size * 4), int(box_size * 4) ),
            PILImage.ANTIALIAS
        )
        img = img.convert('RGB')

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        im = CoreImage(BytesIO(img_byte_arr), ext='png')
        self.mouse.scaled_area.texture = im.texture

    def get_widget_fbo(self, widget):
        scale = 1
        x, y = widget.pos

        if widget.parent != None:
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
            Translate(-x, -y - widget.height, 0)

        fbo.add(widget.canvas)
        fbo.draw()

        pil_img = PILImage.frombytes("RGBA", fbo.size, fbo.pixels).convert('RGB')

        fbo.remove(widget.canvas)

        if widget.parent != None and canvas_parent_index > -1:
            widget.parent.canvas.insert(canvas_parent_index, widget.canvas)

        return pil_img

    def get_pixel(self, x: float, y: float):

        if self.ids.scr_manager.current == '2':
            img = self.get_widget_fbo(self.ids.layout_2)
        else:
            return None

        coords = ( int(x), int(img.height - y) )
        try:
            color = img.getpixel(coords)

            self.increasing_the_area(img, coords)
            self.mouse.label_color.text = str(color)
            print('Area color:', color)
        except IndexError:
            color = ()

        return color

    def change_screen(self, name: str):
        if self.ids.scr_manager.current != name:
            if name == 'home':
                self.ids.scr_manager.transition.direction = 'right'
            else:
                self.ids.scr_manager.transition.direction = 'left'

            self.ids.scr_manager.current = name

    def keyboard_handler(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            self.change_screen('home')
            return True


class PipetteMouse(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor = Image(source='kivygo/icons/transparent.png', size_hint=(None, None), size=[dp(64), dp(64)])
        self.scaled_area = BorderImage(source='kivygo/icons/transparent.png', size_hint=(None, None), size=[dp(90), dp(90)])
        self.label_color = Label(size_hint=(None, None), color=(0.84, 0.78, 0.31, 1))

        Window.add_widget(self.scaled_area)
        Window.add_widget(self.cursor)
        Window.add_widget(self.label_color)

    def set_cursor_icon(self, source: str):
        self.cursor.source = source
        self.cursor.reload()


class PipetteExampleApp(GoApp):

    def build(self):
        return PipetteExample()


if __name__ == "__main__":
    PipetteExampleApp().run()
