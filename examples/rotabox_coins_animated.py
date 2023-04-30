# coin spritesheet borrowed from:
# http://www.williammalone.com/articles/html5-animation-sprite-sheet-photoshop/
import __init__
from kivy.base import runTouchApp
from functools import partial
from random import random
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.clock import Clock
import time
from kivy.properties import ObjectProperty
from kivygo.uix.rotabox import Rotabox

Builder.load_string('''

<Ramp@BoxLayout>:
	size_hint: None, None
	canvas:
		Color:
			rgb: 0.682, 0.251, 0.98
		Rectangle:
			pos: self.pos
			size: self.size

<Root>:
	Ramp:
		id: slotleft
		size: 450, 6
		pos: -50, 120
	Ramp:
		id: slotright
		size: 450, 6
		pos: 430, 120

''')

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


class Root(FloatLayout):

	atlas_coins = ObjectProperty(None)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.coins = []
		self.lastTime = time.time()
		Clock.schedule_interval(self.update, 0.016)

	def update(self, *args):
		if time.time() - self.lastTime > 1:
			self.coins.append(Coin(pos=(self.width * 0.1, self.height * 0.3)))
			self.add_widget(self.coins[-1])
			self.lastTime = time.time()

		for coin in self.coins:
			if coin.x > self.width * 1.1 or coin.y < self.height * -.1:
				self.remove_widget(self.coins.pop(self.coins.index(coin)))

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


if __name__ == '__main__':
	runTouchApp(Root())
