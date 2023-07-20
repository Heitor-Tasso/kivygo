
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.lang.builder import Builder
from kivygo.colors import GoColorBase, GoBackgroundColor


Builder.load_string("""

<GoSwapScreen>:
	background_color: GoColors.no_color
	background_disabled: GoColors.no_color


<GoSwapScreenColor>:
	background_color: GoColors.background_default
	background_hover: GoColors.background_default
	border_color: GoColors.no_color
	border_hover: GoColors.no_color
	border_disabled: GoColors.no_color

""")


class GoSwapScreen(GoBackgroundColor, Screen):

	touch_x = NumericProperty(0)
		
	def on_touch_up(self, touch):
		'''
		Chamada automaticamente pelo kivy,
		serve para mudar de tela de acordo com a posição do toque
		e o movimento.

		Args:
			touch: objeto do kivy que tem as posições do toque

		Returns:
			bool: True ou super().on_touch_up(touch) se o touch foi no widget False se não
		'''
		if not self.collide_point(*touch.pos) or self.touch_x == 0:
			return False
		
		manager = self.parent
		screen_names = manager.screen_names

		if (self.touch_x - touch.x) >= (self.width / 2.5):

			manager.transition.direction = 'left'

			if manager.next() == 'opicional':
				manager.current = screen_names[0]
			else:
				manager.current = manager.next()

		elif (self.touch_x - touch.x) <= -(self.width / 2.5):

			manager.transition.direction = 'right'

			if manager.previous() == 'opicional':
				manager.current = screen_names[len(screen_names)-2]
			else:
				manager.current = manager.previous()
		
		return super().on_touch_up(touch)

	def on_touch_down(self, touch):
		# define o valor de touch_x para ser usado em **on_touch_up**
		if self.collide_point(*touch.pos):
			self.touch_x = touch.x
			return super().on_touch_down(touch)
		
		self.touch_x = 0
		return False


class GoSwapScreenColor(GoColorBase, GoSwapScreen):
	pass
