import __init__
from kivygo.app import kivygoApp
from kivy.lang.builder import Builder
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivygo.uix.androidtabs import AndroidTabsBase, AndroidTabs
from kivygo.uix.button import RippleButton

Builder.load_string('''

#:import hex kivy.utils.get_color_from_hex

<AndroidTabsBar>:
    background_color: app.colors.primary_default

<ExampleTab>:
    padding: "30dp"
    background_color: app.colors.secondary_default
    RippleButton:
        text: root.text
        
''')


class ExampleTab(ColoredBoxLayout, AndroidTabsBase):
    pass


class AndroidTabExampleApp(kivygoApp):
    def build(self):
        android_tabs = AndroidTabs()

        for n in range(1, 6):
            tab = ExampleTab(text=f'TAB {n}')
            android_tabs.add_widget(tab)

        return android_tabs


if __name__ == "__main__":
    AndroidTabExampleApp().run()
