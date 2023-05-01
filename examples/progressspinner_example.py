import __init__
from kivygo.app import kivygoApp
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivygo.uix.progressspinner import (
    ProgressSpinnerBase, ProgressSpinner,
    TextureProgressSpinner, TextureProgressSpinnerBase,
    RotatingTextureProgressSpinner,
)


Builder.load_string('''

<ProgressSpinnerBase>:
    on_touch_down: self.stop_spinning() if self._spinning else self.start_spinning()

<TTextureProgressSpinner@TextureProgressSpinner>:
    texture: app.texture

<TRotatingTextureProgressSpinner@RotatingTextureProgressSpinner>:
    texture: app.texture

<ITextureProgressSpinner@TextureProgressSpinner>:
    source: 'kivygo/images/demoimage.jpg'

<IRotatingTextureProgressSpinner@RotatingTextureProgressSpinner>:
    source: 'kivygo/images/demoimage.jpg'

<MainWidget>:
    BoxLayout:
        orientation: 'vertical'
        
        ProgressSpinner:
        
        TTextureProgressSpinner:
        
        TRotatingTextureProgressSpinner:
    
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            ProgressSpinner:
                color: 0.3, 0.3, 1, 1
                stroke_width: 1
            
            ProgressSpinner:
                speed: 0.5
                color: 1, 0, 0, 1
            
            ProgressSpinner:
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

class TestApp(kivygoApp):
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
