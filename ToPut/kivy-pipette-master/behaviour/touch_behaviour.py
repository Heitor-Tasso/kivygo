from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher


class TouchBehavior(EventDispatcher):
    duration_long_touch = NumericProperty(0.4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_long_touch')
        self.bind(on_touch_down=self.create_clock, on_touch_up=self.delete_clock)
        self.clock = None

    def create_clock(self, widget, touch, *args):
        if self.collide_point(touch.x, touch.y):
            self.clock = Clock.schedule_once(lambda dt: self.clock_callback(touch), self.duration_long_touch)

    def delete_clock(self, widget, touch, *args):
        if self.collide_point(touch.x, touch.y):
            if self.clock:
                self.clock.cancel()

    def clock_callback(self, touch):
        self.dispatch('on_long_touch', touch)

    def on_long_touch(self, touch):
        pass
