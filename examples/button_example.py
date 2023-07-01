import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.gridlayout import ColoredGridLayout
from kivygo.uix.button import (
    RippleButton, RippleToggleButton,
    FadeButton, FadeToggleButton
)

Builder.load_string("""

<ButtonExample>:
	background_color: [1, 1, 1, 0.8]
	padding: "70dp"
    spacing: '30dp'
    rows: 3
    
    RippleButton:
        text: "Normal Rectangle Button"
        # background_color: [0.1, 0.4, 0.1, 1]
	    # background_pressed: [0.1, 0.4, 0.7, 1]
	    # on_cursor_enter: print("CURSOR ENTER [ Normal Rectangle ]")
	    # on_cursor_leave: print("CURSOR LEAVE [ Normal Rectangle ]")
    
	RippleToggleButton:
        text: "Toggle Rectangle Button"
        group: "toggle"
	    # background_color: [0.3, 0.1, 0.7, 1]
	    # background_hover: [0.7, 0.3, 0.5, 1]
	
    FadeButton:
        text: "Normal Rounded Button"
        radius: [dp(50)] * 4
        radius_effect: self.radius
	    # background_color: [0.1, 0.4, 0.1, 1]
	    # background_pressed: [0.1, 0.4, 0.7, 1]
	    # on_press: print("ON_PRESS [ Normal Rectangle ]")
	    # on_release: print("ON_RELEASE [ Normal Rectangle ]")
    
    
    FadeToggleButton:
        text: "Toggle Rounded Button"
	    group: "toggle"
        # background_color: [0.3, 0.1, 0.7, 1]
	    # background_hover: [0.7, 0.3, 0.5, 1]

""")


class ButtonExample(ColoredGridLayout):
	pass

class ButtonExampleApp(kivygoApp):
	def build(self):
		return ButtonExample()
	

if __name__ == "__main__":
	ButtonExampleApp().run()

