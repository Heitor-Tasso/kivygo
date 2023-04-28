import __init__
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivygo.uix.label import AnimatedLabel


Builder.load_string('''

#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<ExampleRoot>:
    orientation: 'vertical'

    AnimatedLabel:
        id: target
        target_text:
            """some text that will be animated"""
        letter_duration: duration.value
        letter_offset: offset.value
        font_size: font_size.value
        transform: transform.text
        on_transform: self.animate()
        on_font_name: self.animate()

    TextInput:
        multiline: False
        size_hint_y: None
        height: self.minimum_height
        on_text_validate:
            target.target_text = self.text
            target.animate()

    Spinner:
        id: transform
        values: ['sky_down', 'pop_in', 'bouncey', 'comes_and_go', 'roll_in']
        text: 'pop_in'
        size_hint_y: None
        height: self.texture_size[1] + dp(10)

    Spinner:
        id: font
        text: target.font_name
        values: app.fonts
        size_hint_y: None
        height: self.texture_size[1] + dp(10)
        on_text:
            f = app.font_paths.get(self.text)
            if f: target.font_name = f

    Button:
        text: 'play'
        on_press: target.animate()
        size_hint_y: None
        height: '48dp'

    GridLayout:
        cols: 3
        Label:
            text: 'letter duration'
        Slider:
            id: duration
            value: 1
            min: 0.01
            max: 10
        Label:
            text: str(duration.value)

        Label:
            text: 'letter time offset'
        Slider:
            id: offset
            value: .1
            min: 0.01
            max: 10
        Label:
            text: str(offset.value)

        Label:
            text: 'font size'
        Slider:
            id: font_size
            value: target.font_size
            value: 50
            min: 5
            max: 100
            step: 1

        Label:
            text: str(target.font_size)

        Label:
            text: 'animation progress'
        Slider:
            id: alpha
            value: target._time
            min: 0
            max: len(target.target_text) * target.letter_offset + target.letter_duration
            on_value:
                target._time = self.value
        Label:
            text: str(alpha.value)

''')



class ExampleRoot(BoxLayout):
	pass


class AnimLabelApp(App):
	fonts = ListProperty([])
	font_paths = DictProperty({})

	def build(self):
		return ExampleRoot()


AnimLabelApp().run()
