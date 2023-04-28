import __init__
from kivygo.app import kivygoApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivygo.uix.shader import ShaderWidget


Builder.load_string("""

<SemiCircle@FloatLayout>
	color: [1, 1, 1, 1]
	angle_start: 0
	angle_end: 360
	canvas.before:

		Color:
			rgba: self.color

		Ellipse:
			angle_start: self.angle_start
			angle_end: self.angle_end
			size: self.size
			pos: self.pos

<MainScreen>:
	name: 'scr 1'
	id: scr1

	ShaderWidget:
		id: shader_widget
		size_hint: [1, 1]

		FloatLayout:
			id: r
			size_hint: [1, 1]

			SemiCircle:
				id: se_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360
				center: [ ( root.x + dp(25) ), ( root.y + dp(25) ) ]
				size_hint: [None, None]
				size: [dp(250), dp(250)]

			SemiCircle:
				id: e_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360

				center: [ \
				root.width - dp(100), \
				root.height - dp(150)]

				size_hint: [None, None]
				size: [dp(250), dp(250)]

			SemiCircle:
				id: s_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360

				center: [ \
				root.center_x - dp(200), \
				root.center_y - dp(100)]

				size_hint: [None, None]
				size: [dp(100), dp(100)]

			SemiCircle:
				id: ft_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360

				center: [ \
				root.center_x - dp(200), \
				root.center_y + dp(250)]

				size_hint: [None, None]
				size: [dp(100), dp(100)]

			SemiCircle:
				id: f_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360

				center: [ \
				root.center_x + dp(150), \
				root.center_y - dp(250)]

				size_hint: [None, None]
				size: [dp(50), dp(50)]

			SemiCircle:
				id: t_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360

				center: [ \
				root.center_x + dp(200), \
				root.center_y + dp(200)]

				size_hint: [None, None]
				size: [dp(50), dp(50)]

			SemiCircle:
				id: first_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360
				center: [ root.center_x, ( root.center_y - dp(150) ) ]
				size_hint: [None, None]
				size: [dp(150), dp(150)]

			SemiCircle:
				id: second_half
				color: [1, 1, 1, 1]
				angle_start: 0
				angle_end: 360
				center: [ root.center_x, ( root.center_y + dp(150) ) ]
				size_hint: [None, None]
				size: [dp(100), dp(100)]

""")


class MainScreen(Screen):
    pass


class ShaderTestApp(kivygoApp):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    ShaderTestApp().run()
