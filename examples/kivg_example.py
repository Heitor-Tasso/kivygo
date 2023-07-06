import __init__
from kivygo.app import GoApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import threading
from kivygo.widgets.kivyg_icon import Kivg


root = Builder.load_string("""

<MYMDIconButton@Button>:
    size_hint: [None, None]
    size: [dp(48), dp(48)]
    on_release:
        app.root.animate(self.svg_icon) \
        if \
        (not "so" in self.svg_icon) \
        and (not "pie" in self.svg_icon) \
        and (not "text" in self.svg_icon) \
        else \
        app.root.shape_animate(self.svg_icon, self.svg_icon.split("/")[-1].split(".")[0]+'_config')


<KivgExample>:
    orientation: "vertical"
    canvas:
        Color:
            rgba: [1, 1, 1, 1]
        Rectangle:
            pos: self.pos
            size: self.size

    AnchorLayout:
        BoxLayout:
            id: svg_area
            size_hint: [None, None]
            size: [256, 256]
    
    GridLayout:
        size_hint_y: None
        height: dp(64)
        id: button_area
        rows: 1
        padding: [dp(4), 0]
        spacing: dp(root.width/40)

        MYMDIconButton:
            svg_icon: "kivygo/icons/kivy.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/python2.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/github3.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/github.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/sublime.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/discord2.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/so.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/text.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/twitter2.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/google3.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/pie_chart.svg"
        
        MYMDIconButton:
            svg_icon: "kivygo/icons/facebook2.svg"


""")

class KivgExample(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.config)
    
    def config(self, *args):
        self.s = Kivg(self.ids.svg_area)

    def show_button_icon(self, *args):
        grid = self.root.ids.button_area
        for b in grid.children:
            s = Kivg(b)
            setattr(b, "s", s)
            Clock.schedule_once(lambda *a: self.draw_filled(s, b.svg_icon))

    def draw_filled(self, s, icon):
        s.draw(icon)

    def draw_path(self, s, icon):
        s.draw(icon, fill=False, outline_width=1)

    def on_start(self):
        t = threading.Thread(target=self.show_button_icon)
        Clock.schedule_once(lambda *args: t.start())

    def animate(self, svg_file):
        self.s.draw(svg_file, animate=True, fill=True, outline_width=1)
    
    def shape_animate(self, svg_file, config):
        self.sf = svg_file
        self.con = config
        print("pie_chart_config -=> ", config)

        pie_chart_config = [
            {"id_":"neck", "from_":"center_y","d":.45, "t":"out_cubic"},
            {"id_":"neck-color","d":0},
            {"id_":"stand", "from_":"center_x", "t":"out_back", "d":.45},
            {"id_":"stand-color", "d":0},
            {"id_":"display", "from_":"center_x", "t":"out_bounce","d":.45},
            {"id_":"display-color","d":0},
            {"id_":"screen", "from_":"center_y", "t":"out_circ","d":.45},
            {"id_":"screen-color", "from_":"left","d":.1},
            {"id_":"bullet1", "from_":"center_x", "d":.2},
            {"id_":"data1", "from_":"left", "d":.3},
            {"id_":"bullet2", "from_":"center_x", "d":.2},
            {"id_":"data2", "from_":"left", "d":.3},
            {"id_":"bullet3", "from_":"center_x", "d":.2},
            {"id_":"data3", "from_":"left", "d":.3},
            {"id_":"pie-full", "from_":"center_y"},
            {"id_":"pie", "from_":"bottom", "t":"out_bounce", "d":.1},
            {"id_":"btn1", "from_": "left"},
            {"id_":"btn2", "from_":"right"},
        ]

        so_config = [
            {"id_": "base", "from_":"center_y", "t":"out_bounce", "d":.4},
            {"id_":"line1", "d":.05},
            {"id_":"line2", "d":.05},
            {"id_":"line3", "d":.05},
            {"id_":"line4", "d":.05},
            {"id_":"line5", "d":.05},
            {"id_":"line6", "d":.05},
        ]

        text_config = [
            {"id_":"k","from_":"center_x", "t":"out_back", "d":.4},
            {"id_":"i","from_":"center_y", "t":"out_bounce", "d":.4},
            {"id_":"v","from_":"top", "t":"out_quint", "d":.4},
            {"id_":"y","from_":"bottom", "t":"out_back", "d":.4}
        ]
        self.s.shape_animate(svg_file, anim_config_list=eval(config))

class KivgExampleApp(GoApp):

    def build(self):
        return KivgExample()


if __name__ == "__main__":
    KivgExampleApp().run()
