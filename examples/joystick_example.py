import __init__

from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivygo.uix.joystick import Joystick
from kivy.app import App


Builder.load_string("""


<StickGroup_Outer@BoxLayout>:
	orientation: 'vertical'
	text: ''

	Label:
		size_hint: (1, 0.2)
		text: root.text
		font_size: min(*self.size) * 0.3
		bold: True
		color: (0.95, 0.95, 0.95, 1)

		canvas.before:
			Color:
				rgba: (0.05, 0.05, 0.05, 1) if root.text else (0.85, 0.85, 0.85, 1)
			Rectangle:
				pos: self.pos
				size: self.size

<StickGroup_Inner@BoxLayout>:
	orientation: 'horizontal'
	padding: 30

<StickGroup_Label@Label>:
	color: (0.6, 0.6, 0.6, 1)

<DemoStick@BoxLayout>:
	orientation: 'vertical'
	text: ''
	sticky: False
	outer_size: 0.9
	inner_size: 0.73
	pad_size: 0.68
	outer_line_width: 0.01
	inner_line_width: 0.01
	pad_line_width: 0.01
	outer_background_color: (0.75, 0.75, 0.75, 1)
	outer_line_color: (0.25, 0.25, 0.25, 1)
	inner_background_color: (0.75, 0.75, 0.75, 1)
	inner_line_color: (0.7,  0.7,  0.7,  1)
	pad_background_color: (0.4,  0.4,  0.4,  1)
	pad_line_color: (0.35, 0.35, 0.35, 1)

	Joystick:
		size_hint: (1, 0.7)
		sticky: root.sticky
		outer_size: root.outer_size
		inner_size: root.inner_size
		pad_size: root.pad_size
		outer_line_width: root.outer_line_width
		inner_line_width: root.inner_line_width
		pad_line_width: root.pad_line_width
		outer_background_color: root.outer_background_color
		outer_line_color: root.outer_line_color
		inner_background_color: root.inner_background_color
		inner_line_color: root.inner_line_color
		pad_background_color: root.pad_background_color
		pad_line_color: root.pad_line_color

	Label:
		size_hint: (1, 0.1)

	Label:
		size_hint: (1, 0.2)
		text: root.text
		font_size: min(*self.size) * 0.5
		color: (0.6, 0.6, 0.6, 1)


<PadDisplay@Label>:
	size_hint: (None, None)
	font_size: min(*self.size) * 0.18
	color: (0.3, 0.3, 0.3, 1)

	canvas.before:
		Color:
			rgba: (0.75, 0.75, 0.75, 1)
		Rectangle:
			pos:  self.pos
			size: self.size


<JoystickDemo>:

	GridLayout:
		size: root.size
		cols: 1
		rows: 5

		canvas.before:
			Color:
				rgba: (0.85, 0.85, 0.85, 1)
			Rectangle:
				pos: self.pos
				size: self.size

		StickGroup_Outer:
			text: 'OPTIONS'

			StickGroup_Inner:
				stick_1: options_Stick_1
				
                DemoStick:
					id: options_Stick_1
					text: 'sticky = False\\n(default)'
					sticky: False
					outer_size: 1
					inner_size: 1
					pad_size: 0.5
					outer_line_width: 0
					inner_line_width: 0
					pad_line_width: 0
					outer_background_color: (0.5,  0.5,  0.5,  1)
					outer_line_color: (0.5,  0.5,  0.5,  1)
					inner_background_color: (0.5,  0.5,  0.5,  1)
					inner_line_color: (0.5,  0.5,  0.5,  1)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.3,  0.3,  0.3,  1)

				DemoStick:
					text: 'sticky = True'
					sticky: True
					outer_size: 1
					inner_size: 1
					pad_size: 0.5
					outer_line_width: 0
					inner_line_width: 0
					pad_line_width: 0
					outer_background_color: (0.5,  0.5,  0.5,  1)
					outer_line_color: (0.5,  0.5,  0.5,  1)
					inner_background_color: (0.5,  0.5,  0.5,  1)
					inner_line_color: (0.5,  0.5,  0.5,  1)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.3,  0.3,  0.3,  1)

		StickGroup_Outer:
			text: '2D STYLES'

			StickGroup_Inner:

				DemoStick:
					outer_size: 1
					inner_size: 0.75
					pad_size: 0.3
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1
					inner_size: 0.75
					pad_size: 0.5
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1
					inner_size: 0.65
					pad_size: 0.7
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.05
					inner_size: 1.05
					pad_size: 0.3
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.05
					inner_size: 1.05
					pad_size: 0.5
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.05
					inner_size: 1.05
					pad_size: 0.7
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 0.75
					inner_size: 0.55
					pad_size: 0.3
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 0.7
					inner_size: 0.5
					pad_size: 0.5
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

		BoxLayout:
			padding: (30, 0)
			size_hint: (1, 0.1)
			StickGroup_Label:
				text: "limit @ outer border"
			StickGroup_Label:
				text: "limit @ outer border"
			StickGroup_Label:
				text: "limit @ outer border"
			StickGroup_Label:
				text: "limit @ inner border"
			StickGroup_Label:
				text: "limit @ inner border"
			StickGroup_Label:
				text: "limit @ inner border"
			StickGroup_Label:
				text: "limit on border"
			StickGroup_Label:
				text: "limit on border"

		StickGroup_Outer:
			text: ''

			StickGroup_Inner:

				DemoStick:
					outer_size: 1
					inner_size: 0.75
					pad_size: 0.3
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.02
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1
					inner_size: 0.7
					pad_size: 0.5
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.025
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1
					inner_size: 0.6
					pad_size: 0.7
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.03
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.05
					inner_size: 1.05
					pad_size: 0.3
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.02
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.05
					inner_size: 1.05
					pad_size: 0.5
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.025
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 1.065
					inner_size: 1.065
					pad_size: 0.7
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.03
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 0.75
					inner_size: 0.75
					pad_size: 0.3
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.02
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

				DemoStick:
					outer_size: 0.7
					inner_size: 0.7
					pad_size: 0.5
					outer_line_width: 0.025
					inner_line_width: 0.015
					pad_line_width: 0.025
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.75, 0.75, 0.75, 1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.4,  0.4,  0.4,  1)
					pad_line_color: (0.35, 0.35, 0.35, 1)

		StickGroup_Outer:
			text: '3D STYLES'

			StickGroup_Inner:

				DemoStick:
					outer_size: 0.5
					inner_size: 0.25
					pad_size: 0.51
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.5,  0.5,  0.5,  1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)

				DemoStick:
					outer_size: 0.65
					inner_size: 0.35
					pad_size: 0.55
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.5,  0.5,  0.5,  1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)

				DemoStick:
					outer_size: 0.9
					inner_size: 0.55
					pad_size: 0.68
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0.5,  0.5,  0.5,  1)
					inner_line_color: (0.7,  0.7,  0.7,  1)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)

				DemoStick:
					outer_size: 0.4
					inner_size: 0.4
					pad_size: 0.6
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0,    0,    0,    0)
					inner_line_color: (0,    0,    0,    0)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)

				DemoStick:
					outer_size: 0.7
					inner_size: 0.7
					pad_size: 0.73
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0, 0, 0, 0)
					inner_line_color: (0, 0, 0, 0)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)

				DemoStick:
					outer_size: 0.85
					inner_size: 0.85
					pad_size: 0.85
					outer_line_width: 0.01
					inner_line_width: 0.01
					pad_line_width: 0.01
					outer_background_color: (0.75, 0.75, 0.75, 1)
					outer_line_color: (0.25, 0.25, 0.25, 1)
					inner_background_color: (0, 0, 0, 0)
					inner_line_color: (0, 0, 0, 0)
					pad_background_color: (0.3,  0.3,  0.3,  1)
					pad_line_color: (0.4,  0.4,  0.4,  1)


	PadDisplay:
		id: pad_display_xy
		size: (root.width/10, root.height/10)
		pos_hint: {'center_x': 0.45, 'center_y': 0.857}

	PadDisplay:
		id: pad_display_rma
		size: (root.width/10, root.height/10)
		pos_hint: {'center_x': 0.55, 'center_y': 0.857}

""")


class JoystickDemo(FloatLayout):
    pass

class JoystickDemoApp(App):
    def build(self):
        self.root = JoystickDemo()
        self._bind_joysticks()

    def _bind_joysticks(self):
        joysticks = self._get_joysticks(self.root)
        for joystick in joysticks:
            joystick.bind(pad=self._update_pad_display)

    def _get_joysticks(self, parent):
        joysticks = []
        if isinstance(parent, Joystick):
            joysticks.append(parent)

        elif hasattr(parent, 'children'):
            for child in parent.children:
                joysticks.extend(self._get_joysticks(child))

        return joysticks

    def _update_pad_display(self, instance, pad):
        x = f'x: {str(pad[0])[0:5]}'
        y = f'\ny: {str(pad[1])[0:5]}'

        r = "radians: " + str(instance.radians)[0:5]
        m = "\nmagnitude: " + str(instance.magnitude)[0:5]
        a = "\nangle: " + str(instance.angle)[0:5]
        self.root.ids.pad_display_xy.text = "".join([x, y])
        self.root.ids.pad_display_rma.text = "".join([r, m, a])


JoystickDemoApp().run()
