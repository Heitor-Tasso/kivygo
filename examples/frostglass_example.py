from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from kivygo.widgets.frostedglass import GoFrostedGlass

Builder.load_string("""

#: import Factory kivy.factory.Factory

<FrostedGlassPopup@ModalView>:
	size_hint: 0.85, 0.4
	frosted_glass_bg: None
	background_color: 0, 0, 0, 0
	GoFrostedGlass:
		pos_hint: {'center_x': 0.5,'center_y': 0.5}
		background: root.frosted_glass_bg
		blur_size: 30
		saturation: 1.0
		luminosity: 1.1
		overlay_color: "#25252515"
		noise_opacity: 0.15
		border_radius:  dp(5), dp(50), dp(5), dp(50)
		outline_color: self.overlay_color
		outline_width: 0.5
		BoxLayout:
			size_hint: 0.8, 0.15
			pos_hint: {'center_x': 0.5,'y': 0.1}
			spacing: dp(20)
			Button:
				text: "CANCEL"
				on_release:
					root.dismiss()
			Button:
				text: "OK"
				on_release:
					root.dismiss()

<FrostGlassExample>:
	ScreenManager:
		id: sm
		Screen1:
			name: 'screen_1'
		Screen2:
			name: 'screen_2'
		Screen3:
			name: 'screen_3'
		Screen4:
			name: 'screen_4'
	GridLayout:
		rows: 2
		cols: 2
		size_hint: (1, None)
		height: dp(90)
		pos_hint: {'top': 0.98}
		Button:
			text: 'STATIC'
			halign: "center"
			on_release:
				root.ids.sm.current = 'screen_1'
		Button:
			text: 'MOVING\\nBACKGROUND'
			halign: "center"
			on_release:
				root.ids.sm.current = 'screen_2'
		Button:
			text: 'MOVING\\nFrostedGlass'
			halign: "center"
			on_release:
				root.ids.sm.current = 'screen_3'
		Button:
			text: 'INSIDE\\nMODALVIEW'
			halign: "center"
			on_release:
				root.ids.sm.current = 'screen_4'


# Example 1
<Screen1>:
	Image:
		id: background_image
		pos_hint: {'center_x': 0.5,'center_y': 0.5}
		source: 'kivygo/icons/bg_example.png'
		size_hint_y: None
		height: self.texture_size[1]
		fit_mode: "scale-down"

	GoFrostedGlass:
		background: background_image
		size_hint: (0.48, 0.48)
		pos_hint: {'top': 1}
		blur_size: 15
		saturation: 1.2
		luminosity: 1.3
		overlay_color: "#ffffff00"
		noise_opacity: 0.1
		border_radius:  0, 0, dp(50), 0
		outline_color: "#000000"
		outline_width: 1

	GoFrostedGlass:
		background: background_image
		size_hint: (0.48, 0.48)
		pos_hint: {'right': 1,'top': 1}
		blur_size: 15
		saturation: 1.3
		luminosity: 1.1
		overlay_color: "#388E3C00"
		noise_opacity: 0.0
		border_radius:  0, 0, 0, dp(50)
		outline_color: "#388E3C00"
		outline_width: 1

	GoFrostedGlass:
		background: background_image
		size_hint: (0.48, 0.48)
		pos_hint: {'right': 1}
		blur_size: 30
		saturation: 1.2
		luminosity: 1.4
		overlay_color: "#D32F2F88"
		noise_opacity: 0.1
		border_radius:  dp(50), 0, 0, 0
		outline_color: "#D32F2F88"
		outline_width: 1

	GoFrostedGlass:
		background: background_image
		size_hint: (0.48, 0.48)
		blur_size: 50
		saturation: 1.2
		luminosity: 1.4
		overlay_color: "#fffff88"
		noise_opacity: 0.18
		border_radius:  0, dp(50), 0, 0
		outline_color: "#1976D2"
		outline_width: 1


# Example 2
<Screen2>:
	ScrollView:
		id: scroll_view
		canvas.before:
			Color:
				rgba: rgba("#757575")
			Rectangle:
				size: self.size
				pos: self.pos
		BoxLayout:
			orientation: 'vertical'
			size_hint: (1, 2)
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"

	GoFrostedGlass:
		pos_hint: {'center_x': 0.5,'center_y': 0.5}
		background: scroll_view
		size_hint: (0.7, 0.35)
		blur_size: 15
		saturation: 1.2
		luminosity: 1.2
		overlay_color: "#F57C0000"
		noise_opacity: 0.12
		border_radius:  dp(20), dp(20), dp(20), dp(20)
		outline_color: "#dedede"
		outline_width: 1


# Example 3
<Screen3>:
	Image:
		id: background_image
		pos_hint: {'center_x': 0.5,'center_y': 0.5}
		source: 'kivygo/icons/bg_example.png'
		size_hint_y: None
		height: self.texture_size[1]
		fit_mode: "scale-down"

	ScrollView:
		id: scroll_view
		pos_hint: {'center_y': 0.5}
		size_hint: (1, 0.4)
		do_scroll_y: False

		BoxLayout:
			size_hint: (6, 1)
			spacing: dp(30)
			padding: dp(10)
			GoFrostedGlass:
				background: background_image
				size_hint_x: None
				width: self.height
				blur_size: 25
				saturation: 1.2
				luminosity: 1.5
				overlay_color: "#76FF004D"
				noise_opacity: 0.1
				border_radius:  self.height/2, self.height/2, self.height/2, self.height/2
				outline_color: "#76FF034D"
				outline_width: 1
			GoFrostedGlass:
				background: background_image
				size_hint: (0.4, 1)
				blur_size: 35
				saturation: 1.2
				luminosity: 1.5
				overlay_color: "#FDD83500"
				noise_opacity: 0.1
				border_radius:  dp(10), dp(10), dp(10), dp(10)
				outline_color: "#FDD83500"
				outline_width: 1
			GoFrostedGlass:
				background: background_image
				size_hint: (0.4, 1)
				blur_size: 15
				saturation: 1.2
				luminosity: 1.2
				overlay_color: "#80808000"
				noise_opacity: 0.0
				border_radius:  dp(200), dp(200), dp(200), dp(200)
				outline_color: "#000000"
				outline_width: 1

			GoFrostedGlass:
				background: background_image
				size_hint: (0.4, 1)
				blur_size: 20
				saturation: 1.2
				luminosity: 1.5
				overlay_color: "#76FF0300"
				noise_opacity: 0.2
				border_radius:  dp(10), dp(10), dp(10), dp(10)
				outline_color: "#76FF03"
				outline_width: 1
			GoFrostedGlass:
				background: background_image
				size_hint: (0.4, 1)
				blur_size: 35
				saturation: 1.2
				luminosity: 1.5
				overlay_color: "#FDD8350"
				noise_opacity: 0.1
				border_radius:  dp(10), dp(10), dp(10), dp(10)
				outline_color: "#FDD835"
				outline_width: 1
			GoFrostedGlass:
				background: background_image
				size_hint: (0.4, 1)
				blur_size: 50
				saturation: 1.8
				luminosity: 1.8
				overlay_color: "#1515159C"
				noise_opacity: 0.1
				border_radius:  dp(10), dp(10), dp(10), dp(10)
				outline_color: "#000000"
				outline_width: 1


# Example 4
<Screen4>:
	popup: Factory.FrostedGlassPopup()
	ScrollView:
		id: scroll_view
		canvas.before:
			Color:
				rgba: rgba("#8BC34A")
			Rectangle:
				size: self.size
				pos: self.pos
		BoxLayout:
			orientation: 'vertical'
			size_hint: (1, 2)
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"
			Image:
				source: 'kivygo/icons/kivy_logo.png'
				fit_mode: "scale-down"

	Button:
		text: "OPEN POPUP"
		size_hint: None, None
		size: dp(150), dp(40)
		pos_hint: {'center_x': 0.5,'center_y': 0.15}
		on_release:
			if root.popup.frosted_glass_bg == None: root.popup.frosted_glass_bg = scroll_view
			root.popup.open()


""")


class FrostGlassExample(FloatLayout):
	pass


class Screen1(Screen):
	pass


class Screen2(Screen):
	pass


class Screen3(Screen):
	pass


class Screen4(Screen):
	pass


class FrostGlassExampleApp(ExampleAppDefault):
	def build(self):
		return FrostGlassExample()

if __name__ == "__main__":
	FrostGlassExampleApp().run()
