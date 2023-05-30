import __init__
from kivygo.app import kivygoApp
from kivy.lang.builder import Builder
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivygo.uix.androidtabs import AndroidTabsBase, AndroidTabs
from kivygo.uix.button import ButtonEffect

Builder.load_string('''

#:import hex kivy.utils.get_color_from_hex

<AndroidTabsBar>:
    background_color: app.primary_color

<ExampleTab>:
    padding: "30dp"
    background_color: app.secondary_color
    ButtonEffect:
        text: root.text
        
''')


class ExampleTab(ColoredBoxLayout, AndroidTabsBase):
    pass


class Example(kivygoApp):
    def build(self):
        android_tabs = AndroidTabs()

        for n in range(1, 6):
            tab = ExampleTab(text=f'TAB {n}')
            android_tabs.add_widget(tab)

        return android_tabs


if __name__ == "__main__":
    Example().run()
