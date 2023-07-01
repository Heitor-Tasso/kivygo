
# -- Window need to be imported after to work with `circular_bar_example.py`
#       in "kivy\app.py", line 932, in _run_prepare
#       AttributeError: 'NoneType' object has no attribute 'add_widget'

# from kivy.config import Config
# Config.set('modules', 'monitor', '')

from kivy.core.window import Window
Window.size = [650, 764]
Window.top = 40

import sys, os

last_path = os.path.abspath(os.path.dirname(os.path.split(__file__)[0]))
sys.path.append(last_path)

from kivygo.app import kivygoApp
from kivygo.uix.boxlayout import ColoredBoxLayout
from kivy.clock import Clock
from kivy.lang.builder import Builder

__clock = Builder.load_string("""

ColoredBoxLayout:
    size_hint: None, None
    height: "30dp"
    background_color: [1, 0, 0, 0.5]
    padding: ["30dp", "0dp", "0dp", "0dp"]
    Label:
        id: clock_label
        color: [1, 1, 1, 1]
        text_size: self.width, None
        halign: "left"
""")

def update_clock(*args):
    root = kivygoApp.get_running_app().root
    lbl = __clock.ids.clock_label
    lbl.text = str(Clock.get_fps())
    __clock.width = root.width
    __clock.pos = [root.x, root.top - __clock.height]

def check_app(*args):
    app = kivygoApp.get_running_app()
    if app == None:
        return None
    
    app.root.padding = 70
    Clock.unschedule(check_app)

    win = app.root.get_root_window()
    win.add_widget(__clock)
    Clock.schedule_interval(update_clock, 0.01)

Clock.schedule_interval(check_app, 0.1)
