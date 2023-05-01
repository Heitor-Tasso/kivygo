import __init__
from kivygo.app import kivygoApp
from kivygo.uix.segment import Segment
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
import random

class SegmentTestApp(kivygoApp):

    def build(self):
        def refresh_task(self, *args):
            seg.value = random.choice('123AbCdEF')
            seg1.value = random.choice('123')

        box = GridLayout(cols=8, padding=20)
        seg = Segment(scale=0.3, value="9.")
        seg1 = Segment(scale=0.8, value="A.")
        
        box.add_widget(seg)
        box.add_widget(seg1)

        Clock.schedule_interval(refresh_task, 1)

        return box
            
if __name__ == '__main__':
    SegmentTestApp().run()
