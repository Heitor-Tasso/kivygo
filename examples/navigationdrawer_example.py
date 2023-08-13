from __init__ import ExampleAppDefault
from kivy.lang.builder import Builder
from kivygo.widgets.navigationdrawer import GoNavigationDrawer


Builder.load_string("""

<NavigationDrawerExample>:
	GoBoxLayout:
		orientation: "vertical"
		GoLabel:
			text: "Panel label"
		GoButton:
			text: "Only a Button"
	
	GoBoxLayout:
		orientation: "vertical"
		background_color: GoColors.background_default
		padding: ["5dp", "10dp", "5dp", "10dp"]
		spacing: "10dp"
		GoLabel:
			text: 
				'[b]Example label filling main panel[/b]\\n\\n[color=ff0000](p' + \
				'ull from left to right!)[/color]\\n\\nIn this example, the le' + \
				'ft panel is a simple boxlayout menu, and this main panel is' + \
				' a BoxLayout with a label and example image.\\n\\nSeveral pre' + \
				'set layouts are available (see buttons below), but users ma' + \
				'y edit every parameter for much more customisation.'
			font_size: '15sp'
			markup: True
			text_size: self.size
			valign: 'top'
		    color: GoColors.at_background_default
			
		GoLabel:
		    size_hint_y: None
		    height: "40dp"
		    text: 'Preset Anims'
		    color: GoColors.at_background_default
		    
		GoBoxLayout:
		    spacing: "10dp"
		    padding: "10dp"
		    GoButton:
		    	text: 'slide_\\nabove_\\nanim'
				on_press: root.set_anim_type('slide_above_anim')
			GoButton:
		    	text: 'slide_\\nabove_\\nsimple'
				on_press: root.set_anim_type('slide_above_simple')
		    GoButton:
		    	text: 'fade_in'
				on_press: root.set_anim_type('fade_in')
		    GoButton:
		    	text: 'reveal_\\nbellow_\\nanim'
				on_press: root.set_anim_type('reveal_below_anim')
		    GoButton:
		    	text: 'reveal_\\nbellow_\\nsimple'
				on_press: root.set_anim_type('reveal_below_simple')	
		
		GoLabel:
		    size_hint_y: None
		    height: "40dp"
		    text: 'Anim Transitions'
		    color: GoColors.at_background_default
		    
		GoBoxLayout:
		    spacing: "10dp"
		    padding: "10dp"
		    GoButton:
		    	text: 'out_cubic'
				on_press: root.set_transition('out_cubic')
			GoButton:
		    	text: 'in_quint'
				on_press: root.set_transition('in_quint')
		    GoButton:
		    	text: 'linear'
				on_press: root.set_transition('linear')
		    GoButton:
		    	text: 'out_sine'
				on_press: root.set_transition('out_sine')
		
		GoBoxLayout:
		    spacing: "10dp"
		    padding: "10dp"
		    size_hint_y: None
		    height: "40dp"    
			GoButton:
				text: 'ANIMATE'
				on_press: root.toggle_state()
			GoButton:
				text: 'JUMP'
				on_press: root.toggle_state(False)
			GoButton:
				text: 'toggle _main_above'
				on_press: root.toggle_main_above()

""")

class NavigationDrawerExample(GoNavigationDrawer):
	
	def set_anim_type(self, name):
		self.anim_type = name


	def set_transition(self, name):
		self.opening_transition = name
		self.closing_transition = name

class NavigationDrawerExampleApp(ExampleAppDefault):
	def build(self):
		return NavigationDrawerExample()
	

if __name__ == "__main__":
	NavigationDrawerExampleApp().run()

