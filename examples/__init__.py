
# -- Window need to be imported after to work with `circular_bar_example.py`
#       in "kivy\app.py", line 932, in _run_prepare
#       AttributeError: 'NoneType' object has no attribute 'add_widget'

from kivy.config import Config
Config.set('modules', 'monitor', '')

from kivy.core.window import Window
Window.size = [700, 814]
Window.top = 40

import sys, os

last_path = os.path.abspath(os.path.dirname(os.path.split(__file__)[0]))
sys.path.append(last_path)

from kivygo.app import kivygoApp


from kivy.clock import Clock

def check_app(*args):
    app = kivygoApp.get_running_app()
    if app == None:
        return None
    
    app.root.padding = 70
    Clock.unschedule(check_app)

Clock.schedule_interval(check_app, 0.1)

