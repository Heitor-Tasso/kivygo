
from kivy.uix.modalview import ModalView
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivygo.uix.label import LabelToScroll
from kivygo.uix.icon import ButtonIcon
from kivygo.uix.button import ButtonEffect
from kivygo.uix.anchorlayout import AnchorLayoutButton


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<BoxPopup>:
	box_background_color: [0, 0, 0, 0]
	box_radius:  [dp(20), dp(20), dp(20), dp(20)]
	box_padding: ['0dp', '15dp', '0dp', '0dp']
	border: [0, 0, 0, 0]
	auto_dismiss: False
	overlay_color: [0, 0, 0, 0]
	background_color: [0, 0, 0, 0]

	ColoredBoxLayout:
		orientation: 'vertical'
		padding: root.box_padding
		background_color: root.box_background_color
		radius: root.box_radius
		id: _colored_box


<ConfirmPopup>:
	msg: "É necessário aceitar os termos de uso!"
	title: "Alerta"
	box_background_color: hex("#038c73")
	padding:
		[dp(330), dp(210), dp(330), dp(210)] \
		if app.root.width > dp(1300) and app.root.height > dp(600) \
		else [dp(130), dp(100), dp(130), dp(100)]
	box_padding: [0, 0, 0, 0]
	overlay_color: [0, 0, 0, 0.7]

	BoxLayout:
		size_hint_y: None
		height: self.minimum_height

		ColoredBoxLayout:
			size_hint_y: None
			height: self.minimum_height
			background_color: hex('#ebeef2')
			radius: [dp(20), dp(20), 0, 0]

			AnchorLayout:
				anchor_y: 'center'
				size_hint_y: None
				height: lb_t.height + dp(10)
				padding: [dp(10), 0, 0, 0]

				LabelToScroll:
					text: root.title
					font_size: "30sp"
					bold: True
					halign: 'left'
					valign: 'center'
					color: hex('#e06031')
					id: lb_t

			AnchorLayoutButton:
				size_hint_y: None
				height: lb_t.parent.height

				ButtonIcon:
					size: ['35dp', '35dp']
					source: app.get_icon('close')
					on_release: root.dismiss()

	AnchorLayout:
		anchor_y: 'center'

		LabelToScroll:
			text: root.msg
			font_size: "20sp"

	AnchorLayout:
		anchor_y: 'center'
		anchor_x: 'center'
		size_hint_y: None
		height: 0 if not self.children else self.children[0].height + dp(30)

		ButtonEffect:
			text: "Continuar"
			size_hint: None, None
			size: '120dp', '55dp'
			radius: [dp(15)]
			background_color: hex('#2c2c2c')
			bold: True
			font_size: '17sp'
			on_release: root.dismiss()

""")


class BoxPopup(ModalView):

	def add_widget(self, widget, *args, **kwargs):
		if isinstance(widget, ColoredBoxLayout):
			return super().add_widget(widget, *args, **kwargs)
		return self.ids._colored_box.add_widget(widget, *args, **kwargs)


class ConfirmPopup(BoxPopup):
	
	msg = StringProperty("É necessário aceitar os termos de uso!")
	title = StringProperty("Alerta")

