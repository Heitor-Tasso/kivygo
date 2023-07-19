
from math import sin, cos, atan2, radians
from kivygo.widgets.widget import GoWidget
from kivy.graphics import Color, SmoothLine, Ellipse
from kivy.properties import NumericProperty, ColorProperty, AliasProperty


class GoRadialSlider(GoWidget):
    '''A :class:`~kivy.uix.widget.Widget` that provides a radial slider.
    '''

    angle = NumericProperty(0)
    '''
    Current angle used for the Radial Slider.
    You can use it for setting the angle of the thumb in the track in range
    0 - 360.
    '''

    track_color = ColorProperty('#ffffff')
    '''Color of the track.
    '''

    thumb_color = ColorProperty('#ffffff')
    '''Color of the thumb.
    '''

    thumb_diameter = NumericProperty(10)
    '''Diameter of the thumb.
    '''

    track_thickness = NumericProperty(2)
    '''Thickness of the track.
    '''

    max_value = NumericProperty(100)
    '''Maximum value allowed for the Radial Slider.
    '''

    min_value = NumericProperty(0)
    '''Minimum value allowed for the Radial Slider.
    '''

    def get_value(self):
        value_range = abs(self.min_value - self.max_value)
        return self.min_value + max(0, min(self.angle, 360))/360 * value_range

    def set_value(self, value):
        self.angle = max(0, min((value - self.min_value)/abs(
            self.max_value - self.min_value) * 360, 360))

    value = AliasProperty(get_value, set_value,
                          bind=('angle', 'min_value', 'max_value'),
                          cache=True)
    '''
    Normalized value inside the :attr:`range` (min_value/max_value).
    You can use it for setting the value betwwen the minimum and maximum value.
    '''

    def get_norm_value(self):
        return self.angle/360

    def set_norm_value(self, value):
        self.angle = value * 360

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'min_value', 'max_value',
                                           'angle'),
                                     cache=True)
    '''
    Normalized value inside the :attr:`range` (min_value/max_value) to
    0-1 range. You can also use it for setting the real value without
    knowing the minimum and maximum value.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._start_angle = 0
        self._end_angle = 360
        self._touch_control = None

        with self.canvas:
            self._track_color = Color(1, 1, 1, 1)
            self._track = SmoothLine(width=2, overdraw_width=2.5,
                                     circle=(self.center_x, self.center_y,
                                             0.5*self.width, 0, 360, 800))
        with self.canvas.after:
            self._thumb_color = Color(1, 1, 1, 1)
            self._thumb = Ellipse(size=self.size, pos=self.pos)
            self._thumb_border = SmoothLine(width=1,
                                            overdraw_width=(2.5),
                                            circle=(self._thumb.pos[0],
                                                    self._thumb.pos[1],
                                                    (self.thumb_diameter/2),
                                                    0, 360, 800))

        self.bind(
            size=self.update_canvas,
            pos=self.update_canvas,
            angle=self.update_canvas
        )

    def update_canvas(self, instance, value):
        self._track_color.rgba = self.track_color
        self._track.width = self.track_thickness

        if self.track_thickness < self.thumb_diameter:
            track_adjustment = self.thumb_diameter
        else:
            track_adjustment = self.track_thickness

        min_dimension = min(self.width/2, self.height/2)

        self._track.circle = (self.center_x, self.center_y, min_dimension -
                              track_adjustment, self._start_angle,
                              self._end_angle, 800)

        self._thumb_color.rgba = self.thumb_color
        self._thumb.size = self.thumb_diameter * 2, self.thumb_diameter * 2

        angle = 90 - max(self._start_angle, min(self.angle, self._end_angle))
        spacing = self.track_thickness - self.thumb_diameter
        spacing = 0 if spacing < 0 else spacing
        self._thumb.pos = [
            self.center_x + (min_dimension - self.thumb_diameter) * \
                cos(radians(angle)) - self.thumb_diameter - spacing * \
                    cos(radians(angle)),
            
            self.center_y + (min_dimension - self.thumb_diameter) * \
                sin(radians(angle)) - self.thumb_diameter - spacing * \
                    sin(radians(angle))
        ]

        self._thumb_border.circle = [
            (self._thumb.pos[0] + self.thumb_diameter),
            (self._thumb.pos[1] + self.thumb_diameter),
            self.thumb_diameter, 0, 360, 800,
        ]

    def on_touch_down(self, touch):
        if self.disabled or self._touch_control != None:
            return None
        
        if not self.collide_point(*touch.pos):
            return None

        # check if the touch is in the dragable thumb
        thumb_limits = (touch.x >= self._thumb.pos[0],
                        touch.x <= self._thumb.pos[0] + self._thumb.size[0],
                        touch.y >= self._thumb.pos[1],
                        touch.y <= self._thumb.pos[1] + self._thumb.size[1]
        )
        if not all(thumb_limits):
            return None

        touch.grab(self)
        self._touch_control = touch
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return None
        
        angle = self.get_angle(touch.x, touch.y) * 180 / (3.14)

        if self._start_angle != 0 or self._end_angle != 360:
            self.angle = self.get_angle_norm(angle)
        else:
            # avoid overscrolling to 0
            if (touch.x + 1 > self.center_x) and self.angle > 270:
                self.angle = 360
            # avoid overscrolling to 360
            elif (touch.x - 1 <= self.center_x) and self.angle < 90:
                self.angle = 0
            else:
                self.angle = self.get_angle_norm(angle)

        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return None
        
        touch.ungrab(self)
        self._touch_control = None
        return True

    def get_angle(self, x, y):
        cx, cy = self.center
        delta_x = x - cx
        delta_y = y - cy
        return atan2(delta_y, delta_x)

    # current angle in range 1 - 360
    def get_angle_norm(self, angle):
        if round(angle) >= 90 and round(angle) <= 180:
            return round(360 + (90 - angle))
        else:
            return round(90 - angle)
