
# -- Window need to be imported after to work with `circular_bar_example.py`
#       in "kivy\app.py", line 932, in _run_prepare
#       AttributeError: 'NoneType' object has no attribute 'add_widget'

# from kivy.config import Config
# Config.set('modules', 'monitor', '')

from kivy.core.window import Window
# Window.size = [650, 764]
Window.size = [650, 550]
Window.top = 130
Window.left = 600

import sys, os

last_path = os.path.abspath(os.path.dirname(os.path.split(__file__)[0]))
sys.path.append(last_path)

from kivygo.app import GoApp
from kivy.properties import BooleanProperty

class ExampleAppDefault(GoApp):

	show_fps = BooleanProperty(True)

