import __init__
from kivygo.app import kivygoApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivygo.uix.rotabox import Rotabox
from functools import partial
from random import random
from kivy.lang import Builder
from kivy.clock import Clock
import time
from kivy.properties import ObjectProperty
from kivygo.uix.rotabox import Rotabox
from kivygo.uix.screenmanager import SwapScreen
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivy.clock import Clock
from kivy.lang import Builder


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex
#:import Rotabox kivygo.uix.rotabox.Rotabox
#:import Clock kivy.clock.Clock

<LogoBox@Rotabox>:
	image: icon
	custom_bounds:
		[[(0.02, 0.977), (0.018, 0.335), (0.212, 0.042), (0.217, 0.408), 
		(0.48, -0.004), (0.988, 0.758), (0.458, 0.665), (0.26, 0.988), 
		(0.268, 0.585)]]
	Image:
		id: icon
		source: 'kivygo/icons/kivy.png'


<Ramp@BoxLayout>:
	size_hint: None, None
	canvas:
		Color:
			rgb: 0.682, 0.251, 0.98
		Rectangle:
			pos: self.pos
			size: self.size

<ManagerScreen>:
	trap: trap
	logo: logo
	canvas:
		Color:
			rgba: hex("#ccccd9")
		Rectangle:
			pos: self.pos
			size: self.size

	SwapScreen:
		name: "screen_1"
		
		Widget:
			Rotabox:
				id: trap
				size: 320, 320
				center: 400, 300
				open_bounds: [0]
				draw_bounds: True
			Rotabox:
				id: logo
				size: 200, 132
				center: 800, 300
				custom_bounds:
					[[(0.013, 0.985), (0.016, 0.407), (0.202, 0.696)],
					[(0.267, 0.346), (0.483, -0.005), (0.691, 0.316), (0.261, 0.975)],
					[(0.539, 0.674), (0.73, 0.37), (0.983, 0.758)],
					[(0.033, 0.315), (0.212, 0.598), (0.218, 0.028)]]
				draw_bounds: True

	SwapScreen:
		name: "screen_2"
		
		FloatLayout:
			RotaButton:
				size: 200, 50
				center: 400, 300
				img_source: 'atlas://data/images/defaulttheme/button'
				allow_rotabox: False
				on_press:
					self.img_source = 'atlas://data/images/defaulttheme/button_pressed'
					self.angle -= 5
					if not self.angle: self.angle -= 0.0000001  # if angle is 0 canvas doesn't update ???
				on_release:
					self.img_source = 'atlas://data/images/defaulttheme/button'

				canvas.before:
					BorderImage:
						source: self.img_source
						pos: self.pos
						size: self.size
				Label:
					size_hint: 1, 1
					text: 'A Rotabox Button'

	SwapScreen:
		name: "screen_3"
		on_enter:
			Clock.schedule_interval(root.update_coins, 0.016)
		
		FloatLayout:
			id: coins_box

			Ramp:
				id: slotleft
				size: 450, 6
				pos: -50, 120
			Ramp:
				id: slotright
				size: 450, 6
				pos: 430, 120
	
				
	SwapScreen:
		name: "screen_4"
		on_enter:
			Clock.schedule_interval(root.update_origin_change, 1/60.0)
		
		Widget:
			Label:
				pos: root.width * 0.35, root.height * 0.85
				text: 'Click to change the point of rotation.'
			LogoBox:
				id: logo_
				pivot: root.center
			Widget:
				id: red_
				color: [1, 0.3, 0.3, 1]
				# size_hint: [None, None]
				size: [10, 10]
				canvas:
					Color:
						rgba: self.color
					Ellipse:
						pos: self.pos
						size: self.size

""")


class RotaButton(ButtonBehavior, Rotabox):
	pass

class Coin(Rotabox):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.draw_bounds = True
		self.speed = random() * 0.3 + 1.5
		Clock.schedule_once(self.config)
	
	def config(self, *args):
		self.source_crop = 'kivygo/config/coins.atlas'
		self.source_bounds = 'kivygo/config/coins.bounds'
		self.turn()

	def turn(self, frame=0, *args):
		if frame > 9:
			frame = 0
		try:
			self.current_image = str(frame)
		except IndexError:
			return None
		else:
			Clock.schedule_once(partial(self.turn, frame + 1), 0.15)

class ManagerScreen(ScreenManager):
	atlas_coins = ObjectProperty(None)
	trap = ObjectProperty(None)
	logo = ObjectProperty(None)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.coins = []
		self.idx = 0
		self.lastTime = time.time()
		Clock.schedule_interval(self.update_open_bounds, 0)

	def update_origin_change(self, *args):
		self.ids.logo_.angle -= 0.5
		self.ids.red_.center = self.ids.logo_.origin

	def on_touch_down(self, touch):
		idx = self.idx
		if idx > 8:
			idx = 0

		self.ids.logo_.origin = self.ids.logo_.get_point(0, idx)
		self.idx = idx + 1
		return super().on_touch_down(touch)

	def update_open_bounds(self, *args):
		this = self.trap
		that = self.logo
		if this.collide_widget(that):
			this.x -= 1
			this.angle += .3
			that.x += .5
		else:
			this.x += .5
			this.angle -= .3
			that.x -= .5
			that.angle -= .6


	def update_coins(self, *args):
		if time.time() - self.lastTime > 1:
			self.coins.append(Coin(pos=(self.width * 0.1, self.height * 0.3)))
			self.ids.coins_box.add_widget(self.coins[-1])
			self.lastTime = time.time()

		for coin in self.coins:
			if coin.x > self.width * 1.1 or coin.y < self.height * -.1:
				self.ids.coins_box.remove_widget(self.coins.pop(self.coins.index(coin)))

			if (coin.collide_widget(self.ids.slotleft)
					or coin.collide_widget(self.ids.slotright)):
			   
				if self.ids.slotleft.top > coin.center_y:
					coin.y -= coin.speed
					continue

				coin.x += coin.speed
				if coin.y < self.height * 0.19:
					coin.y += 1
			else:
				coin.y -= coin.speed


class ExampleUixApp(kivygoApp):
	def build(self):
		return ManagerScreen()
	

if __name__ == "__main__":
	ExampleUixApp().run()

