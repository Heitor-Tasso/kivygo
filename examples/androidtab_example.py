import __init__
from kivygo.app import GoApp
from kivy.lang.builder import Builder
from kivygo.layouts.boxlayout import GoColoredBoxLayout
from kivygo.widgets.androidtabs import AndroidTabsBase, AndroidTabs
from kivygo.widgets.button import GoRippleButton

Builder.load_string('''

#:import hex kivy.utils.get_color_from_hex

<AndroidTabsBar>:
    background_color: GoColors.primary_default

<ExampleTab>:
    padding: "30dp"
    background_color: GoColors.secondary_default
    GoRippleButton:
        text: root.text
        
''')


class ExampleTab(GoColoredBoxLayout, AndroidTabsBase):
    pass


class AndroidTabExampleApp(GoApp):
    def build(self):
        android_tabs = AndroidTabs()

        for n in range(1, 6):
            tab = ExampleTab(text=f'TAB {n}')
            android_tabs.add_widget(tab)

        return android_tabs


if __name__ == "__main__":
    AndroidTabExampleApp().run()
