import __init__
from kivygo.app import kivygoApp
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivygo.uix.circular_bar import CircularProgressBar


Builder.load_string('''

#:import Label kivy.uix.label.Label

<Root>:
	CircularProgressBar:
		size_hint: None, None
		size: [self.widget_size] * 2
		pos: 50, 100
		border_width: 15
		cap_style: "round"
		progress_color: [0, 1, 0, 1]
		background_colour: [0, 0, 1, 1]
		cap_precision: 3
		max_progress: 150
		min_progress: 100
		widget_size: 300
		label: Label(text="I am a label\\ninjected in kivy\\nmarkup string :)\\nEnjoy! --={}=--", font_size=25, halign="center")
		label_color: [0, 0, 1, 1]

	CircularProgressBar:
		size_hint: None, None
		size: [self.widget_size] * 2
		pos: 400, 100
		max_progress: 200
		min_progress: 10
		cap_precision: 100
		label_text: "Ola mundo"

	CircularProgressBar:
		size_hint: None, None
		size: [self.widget_size] * 2
		pos: 650, 100
		cap_style: "square"
		border_width: 5
		progress_color: 0.8, 0.8, 0.5, 1
		cap_precision: 100
		max_progress: 10
		widget_size: 100
        
		label_args: [round(self.progress, 1)]
		label: Label(text="Loading...\\n{}%", font_size=10, halign="center")
		label_color: [1, 0, 0, 1]

''')


class Root(FloatLayout):
    pass


class DemoApp(kivygoApp):

    # Simple animation to show the circular progress bar in action
    def animate(self, dt):
        bar = self.root.children[0]
        if bar.progress < bar.max_progress:
            bar.progress += 0.02
        else:
            bar.progress = bar.min_progress
            Clock.unschedule(self.animate)
            Clock.schedule_once(
                lambda *a: Clock.schedule_interval(self.animate, 0.01), 1)

    def build(self):
        Clock.schedule_once(self.start_animations, 1)
        return Root()

    def start_animations(self, *args):
        # Animate the progress bar
        Clock.schedule_interval(self.animate, 0.01)
        Clock.schedule_once(self.start_animation_first)
        Clock.schedule_once(self.start_animation_second)

    def start_animation_first(self, *args):
        bar = self.root.children[-1]

        bar.progress = bar.min_progress
        anim = Animation(progress=bar.max_progress, duration=4)
        anim.bind(
            on_complete=lambda *a: Clock.schedule_once(self.start_animation_first, 1))
        anim.start(bar)

    def start_animation_second(self, *args):
        bar = self.root.children[-2]

        bar.progress = bar.min_progress
        anim = Animation(progress=bar.max_progress,
                         duration=6, transition="out_quad")
        anim.bind(
            on_complete=lambda *a: Clock.schedule_once(self.start_animation_second, 1))
        anim.start(bar)


if __name__ == '__main__':
    DemoApp().run()
