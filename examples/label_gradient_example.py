import __init__
from kivygo.app import kivygoApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivygo.uix.label import LabelGradient


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import Texture kivy.graphics.texture.Texture


<Manager>:
    LabelGradient:
        text: 'Abba Dabba Doo'
        font_size: 30
        gradient: Texture.create(size=(64, 64))
        size_buf: (64 * 64 * 3)
        buf: bytes([int(x * 255 / self.size_buf) for x in range(self.size_buf)])
        on_kv_post:
            self.gradient.blit_buffer(self.buf, colorfmt='rgb', bufferfmt='ubyte')



""")


class Manager(FloatLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

