import __init__
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivygo.app import kivygoApp
from kivygo.uix.taptargetview import TapTargetView


root = Builder.load_string("""

Screen:

    Image:
        id: logo
        source: "kivygo/icons/kivymd_logo.png"

    BoxLayout:
        id: toolbar
        size_hint_y: None
        elevation: 10
        padding: ["8dp", 0, 0, 0]
        pos_hint: {"top": 1}

        Button:
            id: menu_btn
            pos_hint: {"center_y": .5}

        Widget:
            size_hint_x: None
            width: "25dp"

        Label:
            text: "TapTargetView"
            shorten: True
            font_style: 'H6'

        Button:
            id: search_btn
            text_color: [1, 1, 1, 1]
            pos_hint: {"center_y": .5}

        Button:
            id: info_btn
            text_color: [1, 1, 1, 1]
            pos_hint: {"center_y": .5}

    Label:
        id: lbl
        text: "Congrats! You're" + "\\n" +  "educated now!!"
        opacity: 0
        font_size: "24sp"
        halign: "center"

    FloatLayout:
        size_hint: None, None
        size: 0, 0
        pos: 0, 0
        Button:
            id: add_btn
            size_hint: None, None
            size: '30dp', "30dp"
            pos: 10, 10

""")


class TapTargetViewDemo(kivygoApp):
    def build(self):
        self.screen = root

        ttv4 = TapTargetView(
            widget=self.screen.ids.add_btn,
            outer_radius=dp(320),
            cancelable=True,
            outer_circle_color=[1, 1, 1, 1],
            outer_circle_alpha=0.9,
            title_text="This is an add button",
            description_text="You can cancel it by clicking outside",
            widget_position="left_bottom",
            end=self.complete,
        )

        ttv3 = TapTargetView(
            widget=self.screen.ids.info_btn,
            outer_radius=dp(440),
            outer_circle_color=[1, 1, 1, 1],
            outer_circle_alpha=0.8,
            target_circle_color=[255 / 255, 34 / 255, 212 / 255],
            title_text="This is the info button",
            description_text="No information available yet!",
            widget_position="center",
            title_position="left_bottom",
            end=ttv4.start,
        )

        ttv2 = TapTargetView(
            widget=self.screen.ids.search_btn,
            outer_circle_color=[155 / 255, 89 / 255, 182 / 255],
            target_circle_color=[0.2, 0.2, 0.2],
            title_text="This is the search button",
            description_text="It won't search anything for now.",
            widget_position="center",
            title_position="left_bottom",
            end=ttv3.start,
        )

        ttv1 = TapTargetView(
            widget=self.screen.ids.menu_btn,
            outer_circle_color=[1, 1, 1, 1],
            outer_circle_alpha=0.85,
            title_text="Menu Button",
            description_text="Opens up the drawer",
            widget_position="center",
            title_position="right_bottom",
            end=ttv2.start,
        )
        ttv1.start()

        return self.screen

    def complete(self, *args):
        Animation(opacity=0.3, d=0.2).start(self.screen.ids.logo)
        Animation(opacity=0.3, d=0.2).start(self.screen.ids.lbl)


if __name__ == "__main__":
    TapTargetViewDemo().run()
