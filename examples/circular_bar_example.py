import __init__
from kivygo.app import kivygoApp
from kivygo.uix.anchorlayout import ColoredAnchorLayout
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivygo.uix.circular_bar import CircularProgressBar


Builder.load_string('''

#:import Label kivy.uix.label.Label
#:import hex kivy.utils.get_color_from_hex
#:import Animation kivy.animation.Animation

<Root>:
    orientation: 'vertical'
    padding: "80dp"
    spacing: "40dp"
    background_color: hex('#03A9F4')
    ColoredBoxLayout:
        CircularProgressBar:
            id: last
            max_progress: 200
            min_progress: 10
            cap_precision: 100
            label_text: "Ola mundo"
        CircularProgressBar:
            id: bar
            cap_style: "square"
            border_width: 5
            progress_color: [0.8, 0.8, 0.5, 1]
            cap_precision: 50
            widget_size: 100
            label_args: [round(self.progress)]
            label: Label(text="Loading...\\n{}%", font_size=10, halign="center")
            label_color: [1, 0, 0, 1]
''')


class Root(ColoredAnchorLayout):
    pass


class DemoApp(kivygoApp):

    # Simple animation to show the circular progress bar in action
    def animate(self, dt):
        bar = self.root.ids.last
        if bar.progress < bar.max_progress:
            bar.progress += 0.4
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
        Clock.schedule_once(self.start_animation_second)

    def start_animation_second(self, *args):
        bar = self.root.ids.bar

        bar.progress = bar.min_progress
        anim = Animation(progress=bar.max_progress,
                         duration=6, transition="out_quad")
        anim.bind(
            on_complete=lambda *a: Clock.schedule_once(self.start_animation_second, 1))
        anim.start(bar)


if __name__ == '__main__':
    DemoApp().run()
