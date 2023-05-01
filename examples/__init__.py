from kivy.core.window import Window
from kivy.config import Config
Config.set('modules', 'monitor', '')

import sys
import os

# sys.path.append(os.path.abspath(".."))
last_path = os.path.abspath(os.path.dirname(os.path.split(__file__)[0]))
print("Path -=> ", last_path)
sys.path.append(last_path)
