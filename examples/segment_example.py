from __init__ import ExampleAppDefault
from kivygo.widgets.segment import GoSegment
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
import random

class SegmentTestApp(ExampleAppDefault):

    def build(self):
        def refresh_task(self, *args):
            seg.value = random.choice('123AbCdEF')
            seg1.value = random.choice('123')

        box = GridLayout(cols=8, padding=20)
        seg = GoSegment(scale=0.3, value="9.")
        seg1 = GoSegment(scale=0.8, value="A.")
        
        box.add_widget(seg)
        box.add_widget(seg1)

        Clock.schedule_interval(refresh_task, 1)

        return box
            
if __name__ == '__main__':
    SegmentTestApp().run()
