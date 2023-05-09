import __init__
from kivygo.app import kivygoApp
from kivy.lang import Builder
from kivygo.uix.gridlayout import ColoredGridLayout
from kivygo.uix.button import ButtonEffect, ToggleButtonEffect

Builder.load_string("""

<Manager>:
	background_color: [1, 1, 1, 0.8]
	padding: "70dp"
    spacing: '30dp'
    rows: 3
    
    ButtonEffect:
        text: "Normal Rectangle Button"
        background_color: [[0.1, 0.4, 0.1, 1], [0.1, 0.4, 0.7, 1]]
    
    ButtonEffect:
        text: "Normal Rounded Button"
        radius: [dp(50)] * 4
        radius_effect: self.radius
	    background_color: [[0.1, 0.4, 0.1, 1], [0.1, 0.4, 0.7, 1]]
    
    ToggleButtonEffect:
        text: "Toggle Rectangle Button"
        group: "toggle"
	    down_background_color: [[0.3, 0.1, 0.7, 1], [0.7, 0.3, 0.5, 1]]
    
    ToggleButtonEffect:
        text: "Toggle Rounded Button"
	    group: "toggle"
        down_background_color: [[0.3, 0.1, 0.7, 1], [0.7, 0.3, 0.5, 1]]
	
""")


class Manager(ColoredGridLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

