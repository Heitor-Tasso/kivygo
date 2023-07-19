import __init__
from kivygo.app import GoApp
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivygo.widgets.progressspinner import (
    GoProgressSpinnerBase, GoProgressSpinner,
    GoTextureProgressSpinner, GoTextureProgressSpinnerBase,
    GoRotatingTextureProgressSpinner,
)


Builder.load_string('''

<GoProgressSpinnerBase>:
    on_touch_down: self.stop_spinning() if self._spinning else self.start_spinning()

<TTextureProgressSpinner@GoTextureProgressSpinner>:
    texture: app.texture

<TRotatingTextureProgressSpinner@GoRotatingTextureProgressSpinner>:
    texture: app.texture

<ITextureProgressSpinner@GoTextureProgressSpinner>:
    source: 'kivygo/images/demoimage.jpg'

<IRotatingTextureProgressSpinner@GoRotatingTextureProgressSpinner>:
    source: 'kivygo/images/demoimage.jpg'

<MainWidget>:
    BoxLayout:
        orientation: 'vertical'
        
        GoProgressSpinner:
        
        TTextureProgressSpinner:
        
        TRotatingTextureProgressSpinner:
    
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            GoProgressSpinner:
                color: 0.3, 0.3, 1, 1
                stroke_width: 1
            
            GoProgressSpinner:
                speed: 0.5
                color: 1, 0, 0, 1
            
            GoProgressSpinner:
                speed: 2
                color: 0, 1, 0, 1
        
        BoxLayout:
            TTextureProgressSpinner:
                color: 1, 0, 0, 1
            
            ITextureProgressSpinner:
                stroke_width: 10
            
            ITextureProgressSpinner:
                stroke_length: 20
                
        BoxLayout:
            TRotatingTextureProgressSpinner:
                color: 1, 0, 0, 1
            
            IRotatingTextureProgressSpinner:
                stroke_width: 10
            
            IRotatingTextureProgressSpinner:
                stroke_length: 20
''')

class MainWidget(BoxLayout):
    pass

class TestApp(GoApp):
    texture = ObjectProperty(None)

    def blittex(self, *args):
        rgbpixels = [(x, 0, y, 255) for x in range(256) for y in range(256)]
        pixels = b''.join((b''.join(map(bytearray, pix)) for pix in rgbpixels))
        self.texture = Texture.create(size=(256, 256))
        self.texture.blit_buffer(pixels, colorfmt='rgba', bufferfmt='ubyte')

    def build(self):
        Clock.schedule_once(self.blittex, -1)
        return MainWidget()


if __name__ == "__main__":
    TestApp().run()
