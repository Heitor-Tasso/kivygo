import __init__

from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivygo.uix.navigationdrawer import NavigationDrawer
from kivy.core.window import Window
from kivy.metrics import dp


navigationdrawer = NavigationDrawer()

side_panel = BoxLayout(orientation='vertical')
side_panel.add_widget(Label(text='Panel label'))
popup = Popup(title='Sidebar popup',
			  content=Label(
					text='You clicked the sidebar\npopup button'),
			  size_hint=(0.7, 0.7))
first_button = Button(text='Popup\nbutton')
first_button.bind(on_release=popup.open)
side_panel.add_widget(first_button)
side_panel.add_widget(Button(text='Another\nbutton'))
navigationdrawer.add_widget(side_panel)

label_head = (
	'[b]Example label filling main panel[/b]\n\n[color=ff0000](p'
	'ull from left to right!)[/color]\n\nIn this example, the le'
	'ft panel is a simple boxlayout menu, and this main panel is'
	' a BoxLayout with a label and example image.\n\nSeveral pre'
	'set layouts are available (see buttons below), but users ma'
	'y edit every parameter for much more customisation.')
main_panel = BoxLayout(orientation='vertical')
label_bl = BoxLayout(orientation='horizontal')
label = Label(text=label_head, font_size='15sp',
			  markup=True, valign='top')
label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
label_bl.add_widget(label)
label_bl.add_widget(Widget(size_hint_x=None, width=dp(10)))
main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
main_panel.add_widget(label_bl)
main_panel.add_widget(Widget(size_hint_y=None, height=dp(10)))
navigationdrawer.add_widget(main_panel)
label.bind(size=label.setter('text_size'))


def set_anim_type(name):
	navigationdrawer.anim_type = name


def set_transition(name):
	navigationdrawer.opening_transition = name
	navigationdrawer.closing_transition = name


modes_layout = BoxLayout(orientation='horizontal')
modes_layout.add_widget(Label(text='preset\nanims:'))
slide_an = Button(text='slide_\nabove_\nanim')
slide_an.bind(on_press=lambda j: set_anim_type('slide_above_anim'))
slide_sim = Button(text='slide_\nabove_\nsimple')
slide_sim.bind(on_press=lambda j: set_anim_type('slide_above_simple'))
fade_in_button = Button(text='fade_in')
fade_in_button.bind(on_press=lambda j: set_anim_type('fade_in'))
reveal_button = Button(text='reveal_\nbelow_\nanim')
reveal_button.bind(on_press=lambda j: set_anim_type('reveal_below_anim'))
slide_button = Button(text='reveal_\nbelow_\nsimple')
slide_button.bind(on_press=lambda j: set_anim_type('reveal_below_simple'))
modes_layout.add_widget(slide_an)
modes_layout.add_widget(slide_sim)
modes_layout.add_widget(fade_in_button)
modes_layout.add_widget(reveal_button)
modes_layout.add_widget(slide_button)
main_panel.add_widget(modes_layout)

transitions_layout = BoxLayout(orientation='horizontal')
transitions_layout.add_widget(Label(text='anim\ntransitions'))
out_cubic = Button(text='out_cubic')
out_cubic.bind(on_press=lambda j: set_transition('out_cubic'))
in_quint = Button(text='in_quint')
in_quint.bind(on_press=lambda j: set_transition('in_quint'))
linear = Button(text='linear')
linear.bind(on_press=lambda j: set_transition('linear'))
out_sine = Button(text='out_sine')
out_sine.bind(on_press=lambda j: set_transition('out_sine'))
transitions_layout.add_widget(out_cubic)
transitions_layout.add_widget(in_quint)
transitions_layout.add_widget(linear)
transitions_layout.add_widget(out_sine)
main_panel.add_widget(transitions_layout)

button = Button(text='toggle NavigationDrawer state (animate)',
				size_hint_y=0.2)
button.bind(on_press=lambda j: navigationdrawer.toggle_state())
button2 = Button(text='toggle NavigationDrawer state (jump)',
				 size_hint_y=0.2)
button2.bind(on_press=lambda j: navigationdrawer.toggle_state(False))
button3 = Button(text='toggle _main_above', size_hint_y=0.2)
button3.bind(on_press=navigationdrawer.toggle_main_above)
main_panel.add_widget(button)
main_panel.add_widget(button2)
main_panel.add_widget(button3)

Window.add_widget(navigationdrawer)

runTouchApp()
