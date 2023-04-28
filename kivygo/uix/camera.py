from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
from kivygo.uix.popup import BoxPopup
from kivy.animation import Animation
import time, random, os
from camera4kivy import Preview

from pyzbar import pyzbar
from PIL import Image as PILImage


def get_qrcode(path_img, index=0):
	founded = []
	img = PILImage.open(path_img)
	
	for barcode in pyzbar.decode(img):
		data = barcode.data.decode("utf-8")
		if data not in founded:
			founded.append(data)
	
	if not founded or index == None:
		return None

	return founded[index]


Builder.load_string("""


#:import IconInput kivygo.uix.input.IconInput
#:import ButtonEffect kivygo.uix.button.ButtonEffect
#:import ButtonIcon kivygo.uix.icon.ButtonIcon
#:import AnchorLayoutButton kivygo.uix.anchorlayout.AnchorLayoutButton
#:import hex kivy.utils.get_color_from_hex


<PreviewVCamera>:
	v_size: [0, 0]
	v_pos: [0, 0]

<PlantCamera>:
	on_pre_open: camera.connect_camera()
	on_pre_dismiss: camera.disconnect_camera()
	camera: camera
	sc_prop: [0, 0, 0, 0] # w, h, x, y of scanner
	padding: [0, 0, 0, 0]
	box_padding: [0, 0, 0, 0]
	PreviewVCamera:
		id: camera
		aspect_ratio: '9:16'
		on_size: root._update_camera_options()
		on_pos: root._update_camera_options()
		on_kv_post: root._update_camera_options()
		letterbox_color: hex('#96cfea')
	FloatLayout:
		size_hint: [None, None]
		size: [0, 0]
		BoxLayout:
			size_hint: [None, None]
			size: camera.v_size
			pos: camera.v_pos
			w_scann: (self.x +self.width - root.sc_prop[2] - root.sc_prop[0])
			h_top_scann: ( (self.y + self.height) - (root.sc_prop[3] + root.sc_prop[1]) )
			BoxLayout:
				orientation: 'vertical'
				AnchorLayout:
					size_hint_y: None
					height: '40dp'
					anchor_y: 'center'
					canvas.before:
						Color:
							rgba: hex('#fefefe')
						Rectangle:
							pos: self.pos
							size: self.size
					BoxLayout:
						size_hint_y: None
						height: '30dp'
						BoxLayout:
							size_hint: [None, None]
							size: ['110dp', '30dp']
							AnchorLayoutButton:
								radius: [self.width / 1.7] * 4
								size_hint_y: None
								size: ['60dp', '30dp']
								ButtonIcon:
									size: ['25dp', '25dp']
									# source: icon('flash')
									on_release: root.start_scann()
							Label:
								text: 'Auto'
								bold: True
								color: [0, 0, 0, 1]
								halign: 'left'
								valign: 'center'
								text_size: self.size

						Widget:
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['80dp', '30dp']
							ButtonIcon:
								size: ['25dp', '25dp']
								# source: icon('settings')
								on_release: root.start_scann()
				
				AnchorLayoutButton:
					size_hint_y: None
					height: '40dp'
					width: self.parent.width
					ButtonIcon:
						size: ['25dp', '25dp']
						# source: icon('return')
						on_release: root.dismiss()

				AnchorLayout:
					anchor_x: 'center'
					anchor_y: 'center'
					Widget:
						id: scanner
						size_hint: [None, None]
						size: ['150dp', '150dp']
						on_size: root.sc_prop = [*self.size, *self.pos]
						on_pos: root.sc_prop = [*self.size, *self.pos]

						canvas:
							Color:
								rgba: hex('#207afe')
							Line:
								points: [self.x, (self.y + dp(40)), self.x, self.y, (self.x + dp(40)), self.y]
								width: dp(1.5)
							Line:
								points: [self.x, (self.y + self.height - dp(40)), self.x, (self.y + self.height), (self.x + dp(40)), (self.y + self.height)]
								width: dp(1.5)
							Line:
								points: [(self.x + self.width), (self.y + self.height - dp(40)), (self.x + self.width), (self.y + self.height), (self.x + self.width - dp(40)), (self.y + self.height)]
								width: dp(1.5)
							Line:
								points: [(self.x + self.width), (self.y + dp(40)), (self.x + self.width), self.y, (self.x + self.width - dp(40)), self.y]
								width: dp(1.5)
				
				AnchorLayout:
					size_hint_y: None
					height: '35dp'
					anchor_y: 'center'
					canvas.before:
						Color:
							rgba: hex('#fefefe')[0:-1] + [0.8]
						Rectangle:
							pos: self.pos
							size: self.size
					BoxLayout:
						size_hint_y: None
						height: '25dp'
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['80dp', '25dp']
							ButtonIcon:
								size: ['25dp', '25dp']
								# source: icon('aspect_ratio')
								on_release: root.start_scann()
						Widget:
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['80dp', '25dp']
							ButtonIcon:
								size: ['25dp', '25dp']
								# source: icon('dark_theme')
								on_release: root.start_scann()
				AnchorLayout:
					size_hint_y: None
					height: '100dp'
					anchor_y: 'center'
					canvas.before:
						Color:
							rgba: hex('#e4f2ff')
						Rectangle:
							pos: self.pos
							size: self.size
					BoxLayout:
						size_hint_y: None
						height: '70dp'
						Widget:
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['100dp', '70dp']
							ButtonIcon:
								size: ['60dp', '60dp']
								# source: icon('img')
								on_release: root.start_scann()
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['100dp', '70dp']
							ButtonIcon:
								size: ['70dp', '70dp']
								# source: icon('btn_camera')
								on_release: root.start_scann()
						AnchorLayoutButton:
							radius: [self.width / 1.7] * 4
							size_hint_y: None
							size: ['100dp', '70dp']
							ButtonIcon:
								size: ['60dp', '60dp']
								# source: icon('btn_photos')
								on_release: root.start_scann()
						Widget:


<QRCode>:
	on_pre_open: camera.connect_camera()
	on_pre_dismiss: camera.disconnect_camera()
	camera: camera
	sc_prop: [0, 0, 0, 0] # w, h, x, y of scanner
	padding: [0, 0, 0, 0]
	box_padding: [0, 0, 0, 0]
	PreviewVCamera:
		id: camera
		aspect_ratio: '9:16'
		on_size: root._update_camera_options()
		on_pos: root._update_camera_options()
		on_kv_post: root._update_camera_options()
	FloatLayout:
		size_hint: [None, None]
		size: [0, 0]
		BoxLayout:
			size_hint: [None, None]
			size: camera.v_size
			pos: camera.v_pos
			w_scann: (self.x + self.width - root.sc_prop[2] - root.sc_prop[0])
			h_top_scann: ( (self.y + self.height) - (root.sc_prop[3] + root.sc_prop[1]) )
			canvas.before:
				Color:
					rgba:  [0.1, 0.2, 0.3, 0.4]
				Rectangle:
					pos: [self.x, self.y]
					size: [(self.w_scann or 0), self.height]
				Rectangle:
					pos: [( self.x + self.width - (self.w_scann or 0) ), self.y]
					size: [(self.w_scann or 0), self.height]
				
				Rectangle:
					pos: [( self.x + (self.w_scann or 0) ), ( self.y + self.height - (self.h_top_scann or 0) )]
					size: [(root.sc_prop[0] or 0), (self.h_top_scann or 0)]
				Rectangle:
					pos: [( self.x + (self.w_scann or 0) ), self.y]
					size: [(root.sc_prop[0] or 0), ( (root.sc_prop[3] or 0) - self.y )]

			BoxLayout:
				orientation: 'vertical'
				AnchorLayout:
					anchor_x: 'center'
					anchor_y: 'center'
					Widget:
						id: scanner
						size_hint: [None, None]
						size: ['300dp', '300dp']
						on_size: root.sc_prop = [*self.size, *self.pos]
						on_pos: root.sc_prop = [*self.size, *self.pos]

						canvas:
							Color:
								rgba: hex('#207afe')
							Line:
								points: [self.x, (self.y + dp(60)), self.x, self.y, (self.x + dp(60)), self.y]
								width: dp(3)
							Line:
								points: [self.x, (self.y + self.height - dp(60)), self.x, (self.y + self.height), (self.x + dp(60)), (self.y + self.height)]
								width: dp(3)
							Line:
								points: [(self.x + self.width), (self.y + self.height - dp(60)), (self.x + self.width), (self.y + self.height), (self.x + self.width -dp(60)), (self.y + self.height)]
								width: dp(3)
							Line:
								points: [(self.x + self.width), (self.y + dp(60)), (self.x + self.width), self.y, (self.x + self.width - dp(60)), self.y]
								width: dp(3)

						Icon:
							pos: [(self.parent.x + self.parent.width - self.width - dp(7)), (self.parent.y + dp(7))]
							background_color: [1, 1, 1, 1]
							radius: [self.width / 2] * 4
							size_hint_y: None
							size: ['35dp', '35dp']
							icon_size: ['30dp', '30dp']
							
							# source: icon('resize')
							color: hex('#207afe')
							mipmap: False

							last_touch: 0
							touch_in: False
							on_touch_down:
								if (self.collide_point(*args[1].pos)): self.last_touch = args[1].x
								self.touch_in = True if ( self.collide_point(*args[1].pos) ) else False
							on_touch_up: self.last_touch = 0
							on_touch_move:
								if self.touch_in: scanner.width += (args[1].x - self.last_touch)
								if self.touch_in: scanner.height += (args[1].x - self.last_touch)
								if self.touch_in: self.last_touch = args[1].x
				BoxLayout:
					size_hint_y: None
					height: '70dp'
					padding: ['0dp', '0dp', '0dp', '15dp']
					Widget:
					AnchorLayoutButton:
						background_color: hex('#333333')
						radius: [self.width / 2] * 4
						size_hint_y: None
						size: ['70dp', '70dp']
						ButtonIcon:
							size: ['45dp', '45dp']
							# source: icon('qrcode')
							on_release: root.start_scann()
							color: hex('#313131')
							canvas:
								Color:
									rgba: [1, 1, 1, 1]
								RoundedRectangle:
									pos: self.pos
									size: self.size
									radius: [self.width / 6] * 4
					Widget:
				AnchorLayoutButton:
					size_hint_y: None
					height: '50dp'
					width: self.parent.width
					ButtonIcon:
						size: ['25dp', '25dp']
						# source: icon('return')
						on_release: root.dismiss()

""")


class PreviewVCamera(Preview):
	v_size = ListProperty([0, 0])
	v_pos = ListProperty([0, 0])


class PlantCamera(BoxPopup):

	camera = ObjectProperty(None)
	sc_prop = ListProperty([0, 0, 0, 0])
	started_scan = False
	callback = ObjectProperty(lambda *a: None)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		Clock.schedule_once(self.config)

	def config(self, *args):
		self.camera = self.ids.camera
		
		Window.bind(on_flip=self._update_camera_options)

	def _update_camera_options(self, *args):
		self.camera.v_size = self.camera.preview.view_size
		self.camera.v_pos = self.camera.preview.view_pos
	
	def start_scann(self, *args):
		if self.started_scan: return None

		scanner = self.ids.scanner
		last_size = tuple(map(lambda x: x, scanner.size))
		get_over = lambda *a: self.go_back_scan(last_size)

		anim = Animation(size=tuple(map(lambda x: x*1.3, scanner.size)), d=0.5)
		anim.bind(on_complete=get_over)
		anim.start(scanner)
		self.started_scan = True

	def go_back_scan(self, size):
		scanner = self.ids.scanner
		anim = Animation(size=size, d=0.8)
		anim.bind(on_complete=lambda *a: self.end_scann())
		anim.start(scanner)

	def end_scann(self, *args):
		self.started_scan = False
		Clock.schedule_once(self.next_screen, 1)
	
	def next_screen(self, *args):
		self.dismiss()

class QRCode(BoxPopup):

	camera = ObjectProperty(None)
	sc_prop = ListProperty([0, 0, 0, 0])
	started_scan = False
	callback = ObjectProperty(lambda *a: None)

	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.config)
	
	def config(self, *args):
		self.camera = self.ids.camera
		Window.bind(on_flip=self._update_camera_options)
		
	def _update_camera_options(self, *args):
		self.camera.v_size = self.camera.preview.view_size
		self.camera.v_pos = self.camera.preview.view_pos
	
	def read_qrcode(self, *args):
		path = f'_{int(time.time())}_{random.randint(0, int(time.time()))}.png'
		self.camera.export_to_png(path)
		url = get_qrcode(path)
		os.remove(path)
		return url

	def start_scann(self, *args):
		if self.started_scan: return None

		scanner = self.ids.scanner
		last_size = tuple(map(lambda x: x, scanner.size))
		get_over = lambda *a: self.go_back_scan(last_size)

		anim = Animation(size=tuple(map(lambda x: x*1.3, scanner.size)), d=0.5)
		anim.bind(on_complete=get_over)
		anim.start(scanner)
		self.started_scan = True

	def go_back_scan(self, size):
		scanner = self.ids.scanner
		anim = Animation(size=size, d=0.8)
		anim.bind(on_complete=lambda *a: self.end_scann())
		anim.start(scanner)

	def end_scann(self, *args):
		self.started_scan = False
		result = self.read_qrcode()
		
		if result != None:
			self.dismiss()
			self.callback(result)
