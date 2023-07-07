import __init__
from kivygo.app import GoApp
from kivy.lang.builder import Builder
from kivygo.layouts.boxlayout import GoBoxLayout
from kivygo.widgets.tab import GoTabBase, GoTab


Builder.load_string('''

#:import hex kivy.utils.get_color_from_hex

<GoTabBar>:
    background_color: GoColors.secondary_default

<ExampleTab>:
    padding: "30dp"
    background_color: GoColors.primary_default
    GoRippleButton:
        text: root.text
        
''')


class ExampleTab(GoBoxLayout, GoTabBase):
    pass


class AndroidTabExampleApp(GoApp):
    def build(self):
        android_tabs = GoTab()

        for n in range(1, 6):
            tab = ExampleTab(text=f'TAB {n}')
            android_tabs.add_widget(tab)

        return android_tabs


if __name__ == "__main__":
    AndroidTabExampleApp().run()
