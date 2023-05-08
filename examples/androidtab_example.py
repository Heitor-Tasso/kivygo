import __init__
from kivygo.app import kivygoApp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivygo.uix.androidtabs import AndroidTabsBase, AndroidTabs
from kivygo.uix.button import ButtonEffect

Builder.load_string('''

#:import hex kivy.utils.get_color_from_hex

<AndroidTabsBar>:
    canvas.before:
        Color:
            rgba: hex('#03A9F4')
        Rectangle:
            pos: self.pos
            size: self.size

        # you can add a bit of shade if you want
        Color:
            rgba: [0, 0, 0, 0.3]
        Rectangle:
            pos: [self.pos[0], self.pos[1] - 1]
            size: [self.size[0], 1]
        Color:
            rgba: [0, 0, 0, 0.2]
        Rectangle:
            pos: [self.pos[0], self.pos[1] - 2]
            size: [self.size[0], 1]
        Color:
            rgba: [0, 0, 0, 0.05]
        Rectangle:
            pos: [self.pos[0], self.pos[1] - 3]
            size: [self.size[0], 1]
<MyTab>:
    ButtonEffect:
        text: root.text
        
''')


class MyTab(BoxLayout, AndroidTabsBase):
    pass


class Example(kivygoApp):
    def build(self):
        android_tabs = AndroidTabs()

        for n in range(1, 6):
            tab = MyTab(text=f'TAB {n}')
            android_tabs.add_widget(tab)

        return android_tabs


if __name__ == "__main__":
    Example().run()
