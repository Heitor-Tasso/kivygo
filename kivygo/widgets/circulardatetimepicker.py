
from kivy.animation import Animation
from kivy.clock import Clock
from kivygo.layouts.circularlayout import GoCircularLayout
from kivy.graphics import Line, Color, Ellipse
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty, BoundedNumericProperty,
    ObjectProperty, StringProperty, AliasProperty,
    ListProperty, ReferenceListProperty,
    OptionProperty, BooleanProperty,
    DictProperty
)
from kivygo.layouts.boxlayout import GoBoxLayout
from kivy.uix.label import Label

from math import atan, pi, radians, sin, cos
import datetime


def map_number(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def rgb_to_hex(*color):
    tor = "#"
    for c in color:
        tor += "{:>02}".format(hex(int(c*255))[2:])
    return tor


Builder.load_string("""

<GoNumber>:
    text_size: self.size
    valign: "middle"
    halign: "center"
    font_size: self.height * self.size_factor

<GoCircularNumberPicker>:
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center_x + self.padding[0] - self.padding[2], self.center_y + self.padding[3] - self.padding[1]
            x: self.scale
            y: self.scale

    canvas.after:
        PopMatrix            

<GoCircularTimePicker>:
    orientation: "vertical"
    spacing: "20dp"

    GoAnchorLayout:
        size_hint_y: 1.0 / 3

        GoGridLayout:
            cols: 2
            spacing: "10dp"
            size_hint_x: None
            width: self.minimum_width
           
            Label:
                id: timelabel
                text: root.time_text
                markup: True
                halign: "right"
                valign: "middle"
                size_hint_x: None
                width: self.texture_size[0]
                font_size: self.height * 0.75

            Label:
                id: ampmlabel
                text: root.ampm_text
                markup: True
                halign: "left"
                valign: "middle"
                size_hint_x: None
                width: self.texture_size[0]
                font_size: self.height * 0.3

    GoFloatLayout:
        id: picker_container
        _bound: {}
                
<GoCircularTimePicker>:

<GoCircularHourPicker>:    

""")


class GoNumber(Label):
    """The class used to show the numbers in the selector.
    """

    size_factor = NumericProperty(.5)
    """Font size scale.
    """


class GoCircularNumberPicker(GoCircularLayout):
    """A circular number picker based on GoCircularLayout. A selector will
    help you pick a number. You can also set :attr:`multiples_of` to make
    it show only some numbers and use the space in between for the other
    numbers.
    """

    min = NumericProperty(0)
    """The first value of the range.
    """

    max = NumericProperty(0)
    """The last value of the range. Note that it behaves like range, so
    the actual last displayed value will be :attr:`max` - 1.
    """

    range = ReferenceListProperty(min, max)
    """Packs :attr:`min` and :attr:`max` into a list for convenience. See
    their documentation for further information.
    """

    multiples_of = NumericProperty(1)
    """Only show numbers that are multiples of this number. The other numbers
    will be selectable, but won't have their own label.
    """

    selector_color = ListProperty([0.337, 0.439, 0.490])
    """Color of the number selector. RGB.
    """

    color = ListProperty([1, 1, 1])
    """Color of the number labels and of the center dot. RGB.
    """

    selector_alpha = BoundedNumericProperty(0.3, min=0, max=1)
    """Alpha value for the transparent parts of the selector.
    """

    selected = NumericProperty(None)
    """Currently selected number. defaults to :attr:`min`.
    """

    number_size_factor = NumericProperty(0.5)
    """Font size scale factor fot the :class:`GoNumber`s.
    """

    number_format_string = StringProperty("{}")
    """String that will be formatted with the selected number as the first argument.
    Can be anything supported by :meth:`str.format` (es. "{:02d}").
    """

    scale = NumericProperty(1)
    """Canvas scale factor. Used in :class:`GoCircularTimePicker` transitions.
    """

    _selection_circle = ObjectProperty(None)
    _selection_line = ObjectProperty(None)
    _selection_dot = ObjectProperty(None)
    _selection_dot_color = ObjectProperty(None)
    _selection_color = ObjectProperty(None)
    _center_dot = ObjectProperty(None)
    _center_color = ObjectProperty(None)


    def _get_items(self):
        return self.max - self.min
    
    items = AliasProperty(_get_items, None)


    def _get_shown_items(self):
        c = 0
        for i in range(*self.range):
            if i % self.multiples_of == 0:
                c += 1
        return c
    shown_items = AliasProperty(_get_shown_items, None)

    def __init__(self, **kw):
        self._trigger_genitems = Clock.create_trigger(self._genitems, -1)
        self.bind(
            min=self._trigger_genitems,
            max=self._trigger_genitems,
            multiples_of=self._trigger_genitems
        )
        
        super().__init__(**kw)
        
        self.selected = self.min
        self.bind(
            selected=self.on_selected,
            pos=self.on_selected,
            size=self.on_selected
        )

        cx = self.center_x + self.padding[0] - self.padding[2]
        cy = self.center_y + self.padding[3] - self.padding[1]
        sx, sy = self.pos_for_number(self.selected)
        epos = [i - (self.delta_radii * self.number_size_factor) for i in (sx, sy)]
        esize = [self.delta_radii * self.number_size_factor * 2]*2
        dsize = [i * .3 for i in esize]
        dpos = [i + esize[0] / 2. - dsize[0] / 2. for i in epos]
        csize = [i * .05 for i in esize]
        cpos = [i - csize[0] / 2. for i in (cx, cy)]
        dot_alpha = 0 if self.selected % self.multiples_of == 0 else 1
        color = list(self.selector_color)

        with self.canvas:
            self._selection_color = Color(*(color + [self.selector_alpha]))
            self._selection_circle = Ellipse(pos=epos, size=esize)
            self._selection_line = Line(points=[cx, cy, sx, sy])
            self._selection_dot_color = Color(*(color + [dot_alpha]))
            self._selection_dot = Ellipse(pos=dpos, size=dsize)
            self._center_color = Color(*self.color)
            self._center_dot = Ellipse(pos=cpos, size=csize)

        self.bind(selector_color=lambda ign, c: setattr(self._selection_color, "rgba", c + [self.selector_alpha]))
        self.bind(selector_color=lambda ign, c: setattr(self._selection_dot_color, "rgb", c))
        self.bind(color=lambda ign, c: setattr(self._center_color, "rgb", c))
        Clock.schedule_once(self._genitems)
        Clock.schedule_once(self.on_selected) # Just to make sure pos/size are set

    def _genitems(self, *a):
        self.clear_widgets()
        for i in range(*self.range):
            if i % self.multiples_of != 0:
                continue
            n = GoNumber(text=self.number_format_string.format(i), size_factor=self.number_size_factor, color=self.color)
            self.bind(color=n.setter("color"))
            self.add_widget(n)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return None
        
        touch.grab(self)
        self.selected = self.number_at_pos(*touch.pos)

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_move(touch)
        self.selected = self.number_at_pos(*touch.pos)

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_up(touch)
        touch.ungrab(self)

    def on_selected(self, *a):
        cx = self.center_x + self.padding[0] - self.padding[2]
        cy = self.center_y + self.padding[3] - self.padding[1]
        sx, sy = self.pos_for_number(self.selected)
        epos = [i - (self.delta_radii * self.number_size_factor) for i in (sx, sy)]
        esize = [self.delta_radii * self.number_size_factor * 2]*2
        dsize = [i * .3 for i in esize]
        dpos = [i + esize[0] / 2. - dsize[0] / 2. for i in epos]
        csize = [i * .05 for i in esize]
        cpos = [i - csize[0] / 2. for i in (cx, cy)]
        dot_alpha = 0 if self.selected % self.multiples_of == 0 else 1

        if self._selection_circle:
            self._selection_circle.pos = epos
            self._selection_circle.size = esize
        
        if self._selection_line:
            self._selection_line.points = [cx, cy, sx, sy]
        
        if self._selection_dot:
            self._selection_dot.pos = dpos
            self._selection_dot.size = dsize
        
        if self._selection_dot_color:
            self._selection_dot_color.a = dot_alpha
        
        if self._center_dot:
            self._center_dot.pos = cpos
            self._center_dot.size = csize

    def pos_for_number(self, n):
        """Returns the center x, y coordinates for a given number.
        """
        if self.items == 0:
            return [0, 0]
        
        radius = min(self.width-self.padding[0]-self.padding[2], self.height-self.padding[1]-self.padding[3]) / 2.
        middle_r = radius * sum(self.radius_hint) / 2.
        cx = self.center_x + self.padding[0] - self.padding[2]
        cy = self.center_y + self.padding[3] - self.padding[1]
        sign = +1.
        angle_offset = radians(self.start_angle)
        if self.direction == 'cw':
            angle_offset = 2 * pi - angle_offset
            sign = -1.
        quota = 2*pi / self.items
        mult_quota = 2*pi / self.shown_items
        angle = angle_offset + n * sign * quota

        if self.items == self.shown_items:
            angle += quota / 2
        else:
            angle -= mult_quota / 2

        # kived: looking it up, yes. x = cos(angle) * radius + centerx; y = sin(angle) * radius + centery
        x = cos(angle) * middle_r + cx
        y = sin(angle) * middle_r + cy

        return [x, y]

    def number_at_pos(self, x, y):
        """Returns the number at a given x, y position. The number is found
        using the widget's center as a starting point for angle calculations.

        Not thoroughly tested, may yield wrong results.
        """
        if self.items == 0:
            return self.min

        cx = self.center_x + self.padding[0] - self.padding[2]
        cy = self.center_y + self.padding[3] - self.padding[1]
        lx = x - cx
        ly = y - cy
        quota = 2*pi / self.items
        mult_quota = 2*pi / self.shown_items
        if lx == 0 and ly > 0:
            angle = pi/2
        elif lx == 0 and ly < 0:
            angle = 3*pi/2
        else:
            angle = atan(ly/lx)
            if lx < 0 and ly > 0:
                angle += pi
            if lx > 0 and ly < 0:
                angle += 2*pi
            if lx < 0 and ly < 0:
                angle += pi
        angle += radians(self.start_angle)
        if self.direction == "cw":
            angle = 2*pi - angle
        if mult_quota != quota:
            angle -= mult_quota / 2
        if angle < 0:
            angle += 2*pi
        elif angle > 2*pi:
            angle -= 2*pi

        return min(int(angle / quota) + self.min, self.max-1)


class GoCircularMinutePicker(GoCircularNumberPicker):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 0
        self.max = 60
        self.multiples_of = 5
        self.number_format_string = "{:02d}"
        self.direction = "cw"
        self.bind(shown_items=self._update_start_angle)
        Clock.schedule_once(self._update_start_angle)
        Clock.schedule_once(self.on_selected)

    def _update_start_angle(self, *a):
        self.start_angle = -(360. / self.shown_items / 2) - 90


class GoCircularHourPicker(GoCircularNumberPicker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min = 1
        self.max = 13
        self.multiples_of = 1
        self.number_format_string = "{}"
        self.direction = "cw"
        self.bind(shown_items=self._update_start_angle)
        Clock.schedule_once(self._update_start_angle)
        Clock.schedule_once(self.on_selected)

    def _update_start_angle(self, *a):
        self.start_angle = (360.0 / self.shown_items / 2) - 90


class GoCircularTimePicker(GoBoxLayout):
    """Widget that makes use of :class:`GoCircularHourPicker` and
    :class:`GoCircularMinutePicker` to create a user-friendly, animated
    time picker like the one seen on Android.

    See module documentation for more details.
    """

    hours = NumericProperty(0)
    """The hours, in military format (0-23).

    :attr:`hours` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0 (12am).
    """

    minutes = NumericProperty(0)
    """The minutes.
    """

    time_list = ReferenceListProperty(hours, minutes)
    """Packs :attr:`hours` and :attr:`minutes` in a list for convenience.
    """

    time_format = StringProperty("[color={hours_color}][ref=hours]{hours}[/ref][/color]:[color={minutes_color}][ref=minutes]{minutes:02d}[/ref][/color]")
    """String that will be formatted with the time and shown in the time label.
    Can be anything supported by :meth:`str.format`. Make sure you don't
    remove the refs. See the default for the arguments passed to format.

    :attr:`time_format` is a :class:`~kivy.properties.StringProperty` and
    defaults to "[color={hours_color}][ref=hours]{hours}[/ref][/color]:[color={minutes_color}][ref=minutes]{minutes:02d}[/ref][/color]".
    """

    ampm_format = StringProperty("[color={am_color}][ref=am]AM[/ref][/color]\n[color={pm_color}][ref=pm]PM[/ref][/color]")
    """String that will be formatted and shown in the AM/PM label.
    Can be anything supported by :meth:`str.format`. Make sure you don't
    remove the refs. See the default for the arguments passed to format.

    :attr:`ampm_format` is a :class:`~kivy.properties.StringProperty` and
    defaults to "[color={am_color}][ref=am]AM[/ref][/color]\n[color={pm_color}][ref=pm]PM[/ref][/color]".
    """

    picker = OptionProperty("hours", options=("minutes", "hours"))
    """Currently shown time picker. Can be one of "minutes", "hours".
    """

    selector_color = ListProperty([0.337, 0.439, 0.490])
    """Color of the number selector and of the highlighted text. RGB.
    """

    color = ListProperty([1, 1, 1])
    """Color of the number labels and of the center dot. RGB.
    """

    selector_alpha = BoundedNumericProperty(0.3, min=0, max=1)
    """Alpha value for the transparent parts of the selector.
    """

    _am = BooleanProperty(True)
    _h_picker = ObjectProperty(None)
    _m_picker = ObjectProperty(None)
    _bound = DictProperty({})


    def _get_time(self):
        return datetime.time(*self.time_list)
    
    def _set_time(self, dt):
        self.time_list = [dt.hour, dt.minute]
    
    time = AliasProperty(_get_time, _set_time, bind=("time_list",))
    """Selected time as a datetime.time object.
    """


    def _get_picker(self):
        if self.picker == "hours":
            return self._h_picker
        return self._m_picker
    
    _picker = AliasProperty(_get_picker, None)


    def _get_time_text(self):
        hc = rgb_to_hex(*self.selector_color) if self.picker == "hours" else rgb_to_hex(*self.color)
        mc = rgb_to_hex(*self.selector_color) if self.picker == "minutes" else rgb_to_hex(*self.color)
        h = self.hours == 0 and 12 or self.hours <= 12 and self.hours or self.hours - 12
        m = self.minutes
        return self.time_format.format(hours_color=hc, minutes_color=mc, hours=h, minutes=m)
    
    time_text = AliasProperty(_get_time_text, None, bind=("hours", "minutes", "time_format", "picker"))


    def _get_ampm_text(self):
        amc = rgb_to_hex(*self.selector_color) if self._am else rgb_to_hex(*self.color)
        pmc = rgb_to_hex(*self.selector_color) if not self._am else rgb_to_hex(*self.color)
        return self.ampm_format.format(am_color=amc, pm_color=pmc)
    
    ampm_text = AliasProperty(_get_ampm_text, None, bind=("hours", "ampm_format", "_am"))


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.hours >= 12:
            self._am = False
        
        self.bind(time_list=self.on_time_list, picker=self._switch_picker, _am=self.on_ampm)
        self._h_picker = GoCircularHourPicker()
        self._m_picker = GoCircularMinutePicker()
        Clock.schedule_once(self.on_selected)
        Clock.schedule_once(self.on_time_list)
        Clock.schedule_once(self._init_later)
        Clock.schedule_once(lambda *a: self._switch_picker(noanim=True))
        
    def _init_later(self, *args):
        self.ids.timelabel.bind(on_ref_press=self.on_ref_press)
        self.ids.ampmlabel.bind(on_ref_press=self.on_ref_press)

    def on_ref_press(self, ign, ref):
        if ref == "hours":
            self.picker = "hours"
        
        elif ref == "minutes":
            self.picker = "minutes"
        
        elif ref == "am":
            self._am = True
        
        elif ref == "pm":
            self._am = False

    def on_selected(self, *a):
        if not self._picker:
            return None
        
        if self.picker == "hours":
            hours = self._picker.selected if self._am else self._picker.selected + 12
            if hours == 24 and not self._am:
                hours = 12
            
            elif hours == 12 and self._am:
                hours = 0
            
            self.hours = hours
        elif self.picker == "minutes":
            self.minutes = self._picker.selected

    def on_time_list(self, *a):
        if not self._picker:
            return None
        
        if self.picker == "hours":
            self._picker.selected = self.hours == 0 and 12 or self._am and self.hours or self.hours - 12
        
        elif self.picker == "minutes":
            self._picker.selected = self.minutes

    def on_ampm(self, *a):
        if self._am:
            self.hours = self.hours if self.hours <  12 else self.hours - 12
        else:
            self.hours = self.hours if self.hours >= 12 else self.hours + 12

    def _switch_picker(self, *args, **kwargs):
        noanim = "noanim" in kwargs
        if noanim:
            noanim = kwargs["noanim"]

        try:
            container = self.ids.picker_container
        except (AttributeError, NameError):
            Clock.schedule_once(lambda *a: self._switch_picker(noanim=noanim))

        if self.picker == "hours":
            picker = self._h_picker
            prevpicker = self._m_picker
        
        elif self.picker == "minutes":
            picker = self._m_picker
            prevpicker = self._h_picker

        if len(self._bound) > 0:
            prevpicker.unbind(selected=self.on_selected)
            self.unbind(**self._bound)
        
        picker.bind(selected=self.on_selected)
        self._bound = {
            "selector_color": picker.setter("selector_color"),
            "color":          picker.setter("color"),
            "selector_alpha": picker.setter("selector_alpha")
        }
        self.bind(**self._bound)
        
        if len(container._bound) > 0:
            container.unbind(**container._bound)
        
        container._bound = {"size": picker.setter("size"), "pos":  picker.setter("pos")}
        container.bind(**container._bound)

        picker.pos = container.pos
        picker.size = container.size
        picker.selector_color = self.selector_color
        picker.color = self.color
        picker.selector_alpha = self.selector_alpha

        if noanim:
            if prevpicker in container.children:
                container.remove_widget(prevpicker)
            
            if picker.parent:
                picker.parent.remove_widget(picker)
            
            container.add_widget(picker)
        else:
            if prevpicker in container.children:
                anim = Animation(scale=1.5, d=.5, t="in_back") & Animation(opacity=0, d=.5, t="in_cubic")
                anim.start(prevpicker)
                Clock.schedule_once(lambda *a: container.remove_widget(prevpicker), .5)
            
            picker.scale = 1.5
            picker.opacity = 0
            if picker.parent:
                picker.parent.remove_widget(picker)
            
            container.add_widget(picker)
            anim = Animation(scale=1, d=.5, t="out_back") & Animation(opacity=1, d=.5, t="out_cubic")
            Clock.schedule_once(lambda *a: anim.start(picker), .3)
