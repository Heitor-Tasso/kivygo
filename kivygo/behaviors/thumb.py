import os
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import RenderContext, RoundedRectangle

from kivy.properties import (
    AliasProperty, BoundedNumericProperty,
    ColorProperty, ListProperty,
    NumericProperty, VariableListProperty,
    StringProperty, BooleanProperty,
)

from kivy.graphics import (
    Color, Ellipse,
    StencilPop, StencilPush,
    StencilUnUse, StencilUse,
)

from kivygo.utils import root_path, do_correction_path
from kivygo.behaviors.button import ToggleButtonBehavior


class CommonRipple():

    ripple_rad_default = NumericProperty(1)
    """The starting value of the radius of the ripple effect.
    """

    ripple_color = ColorProperty(None)
    """Ripple color in (r, g, b, a) format.
    """

    ripple_alpha = NumericProperty(0.5)
    """Alpha channel values for ripple effect.
    """

    ripple_scale = NumericProperty(None)
    """Ripple effect scale.
    """

    ripple_duration_in_fast = NumericProperty(0.3)
    """Ripple duration when touching to widget.
    """

    ripple_duration_in_slow = NumericProperty(2)
    """Ripple duration when long touching to widget.
    """

    ripple_duration_out = NumericProperty(0.3)
    """The duration of the disappearance of the wave effect.
    """

    ripple_canvas_after = BooleanProperty(True)
    """The ripple effect is drawn above/below the content.
    """

    ripple_func_in = StringProperty("out_quad")
    """Type of animation for ripple in effect.
    """

    ripple_func_out = StringProperty("out_quad")
    """Type of animation for ripple out effect.
    """

    _ripple_rad = NumericProperty()
    _doing_ripple = BooleanProperty(False)
    _finishing_ripple = BooleanProperty(False)
    _fading_out = BooleanProperty(False)
    _no_ripple_effect = BooleanProperty(False)
    _round_rad = ListProperty([0, 0, 0, 0])

    def lay_canvas_instructions(self):
        raise NotImplementedError

    def start_ripple(self) -> None:
        if not self._doing_ripple:
            self._doing_ripple = True
            anim = Animation(
                _ripple_rad=self.finish_rad,
                t="linear",
                duration=self.ripple_duration_in_slow,
            )
            anim.bind(on_complete=self.fade_out)
            anim.start(self)

    def finish_ripple(self) -> None:
        if self._doing_ripple and not self._finishing_ripple:
            self._finishing_ripple = True
            self._doing_ripple = False
            Animation.cancel_all(self, "_ripple_rad")
            anim = Animation(
                _ripple_rad=self.finish_rad,
                t=self.ripple_func_in,
                duration=self.ripple_duration_in_fast,
            )
            anim.bind(on_complete=self.fade_out)
            anim.start(self)

    def fade_out(self, *args) -> None:
        rc = self.ripple_color
        if not self._fading_out:
            self._fading_out = True
            Animation.cancel_all(self, "ripple_color")
            anim = Animation(
                ripple_color=[rc[0], rc[1], rc[2], 0.0],
                t=self.ripple_func_out,
                duration=self.ripple_duration_out,
            )
            anim.bind(on_complete=self.anim_complete)
            anim.start(self)

    def anim_complete(self, *args) -> None:
        self._doing_ripple = False
        self._finishing_ripple = False
        self._fading_out = False

        if not self.ripple_canvas_after:
            canvas = self.canvas.before
        else:
            canvas = self.canvas.after

        canvas.remove_group("circular_ripple_behavior")
        canvas.remove_group("rectangular_ripple_behavior")

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if touch.is_mouse_scrolling:
            return False
        
        if not self.collide_point(touch.x, touch.y):
            return False
        
        if not self.disabled:
            self.call_ripple_animation_methods(touch)
            if isinstance(self, ToggleButtonBehavior):
                return super().on_touch_down(touch)
            else:
                return True

    def call_ripple_animation_methods(self, touch) -> None:
        if self._doing_ripple:
            Animation.cancel_all(
                self, "_ripple_rad", "ripple_color", "rect_color"
            )
            self.anim_complete()
        self._ripple_rad = self.ripple_rad_default
        self.ripple_pos = (touch.x, touch.y)

        if self.ripple_color:
            pass
        elif hasattr(self, "theme_cls"):
            self.ripple_color = self.theme_cls.ripple_color
        else:
            # If no theme, set Gray 300.
            self.ripple_color = [
                0.8784313725490196,
                0.8784313725490196,
                0.8784313725490196,
                self.ripple_alpha,
            ]
        self.ripple_color[3] = self.ripple_alpha
        self.lay_canvas_instructions()
        self.finish_rad = max(self.width, self.height) * self.ripple_scale
        self.start_ripple()

    def on_touch_move(self, touch, *args):
        if not self.collide_point(touch.x, touch.y):
            if not self._finishing_ripple and self._doing_ripple:
                self.finish_ripple()

        return super().on_touch_move(touch, *args)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y) and self._doing_ripple:
            self.finish_ripple()

        return super().on_touch_up(touch)

    def _set_ellipse(self, instance, value):
        self.ellipse.size = (self._ripple_rad, self._ripple_rad)

    def _set_color(self, instance, value):
        self.col_instruction.a = value[3]


class CircularRippleBehavior(CommonRipple):

    ripple_scale = NumericProperty(1)
    """See :class:`~CommonRipple.ripple_scale`.
    """

    def lay_canvas_instructions(self) -> None:
        if self._no_ripple_effect:
            return None

        with self.canvas.after if self.ripple_canvas_after else self.canvas.before:
            StencilPush(group="circular_ripple_behavior")
            self.stencil = Ellipse(
                size=[n * self.ripple_scale for n in self.size],
                pos=(
                    self.center_x - (self.width * self.ripple_scale) / 2,
                    self.center_y - (self.height * self.ripple_scale) / 2,
                ),
                group="circular_ripple_behavior",
            )
            StencilUse(group="circular_ripple_behavior")
            self.col_instruction = Color(rgba=self.ripple_color)
            self.ellipse = Ellipse(
                size=(self._ripple_rad, self._ripple_rad),
                pos=(
                    self.center_x - self._ripple_rad / 2.0,
                    self.center_y - self._ripple_rad / 2.0,
                ),
                group="circular_ripple_behavior",
            )
            StencilUnUse(group="circular_ripple_behavior")
            Ellipse(
                pos=self.pos, size=self.size,
                group="circular_ripple_behavior"
            )
            StencilPop(group="circular_ripple_behavior")
            self.bind(
                ripple_color=self._set_color,
                _ripple_rad=self._set_ellipse
            )

    def _set_ellipse(self, instance, value):
        super()._set_ellipse(instance, value)
        if self.ellipse.size[0] > self.width * 0.6 and not self._fading_out:
            self.fade_out()

        self.ellipse.pos = (
            self.center_x - self._ripple_rad / 2.0,
            self.center_y - self._ripple_rad / 2.0,
        )


class CommonElevationBehavior(Widget):

    elevation = BoundedNumericProperty(0, min=0, errorvalue=0)
    """Elevation of the widget.
    """

    shadow_radius = VariableListProperty([0], length=4)
    """Radius of the corners of the shadow.
    """

    shadow_softness = NumericProperty(12)
    """Softness of the shadow.
    """

    shadow_softness_size = BoundedNumericProperty(2, min=2)
    """The value of the softness of the shadow.
    """

    shadow_offset = ListProperty((0, 2))
    """Offset of the shadow.
    """

    shadow_color = ColorProperty([0, 0, 0, 0.6])
    """Offset of the shadow.
    """

    _elevation = 0
    _shadow_color = [0.0, 0.0, 0.0, 0.0]


    def _get_widget_pos(self, *args):
        widget_pos = self.to_window(*self.pos)
        # To list, so it can be compared to self.pos directly.
        return list(widget_pos)

    def _set_widget_pos(self, value):
        self.widget_pos = value

    widget_pos = AliasProperty(_get_widget_pos, _set_widget_pos)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.context = RenderContext(use_parent_projection=True)
        with self.context:
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)

        Clock.schedule_once(self.set_shader_string)
        Clock.schedule_once(lambda x: self.on_elevation(self, self.elevation))
        Window.bind(on_draw=self.on_pos)

    def get_shader_string(self):
        shader_string = ""
        for name_file in ["header.frag", "elevation.frag", "main.frag"]:
            path = do_correction_path(os.path.join(root_path, "elevation", name_file))
            with open(path, encoding="utf-8") as file:
                shader_string += f"{file.read()}\n\n"

        return shader_string

    def set_shader_string(self, *args) -> None:
        self.context["shadow_radius"] = list(map(float, self.shadow_radius))
        self.context["shadow_softness"] = float(self.shadow_softness)
        self.context["shadow_color"] = list(map(float, self.shadow_color))[:-1] + [float(self.opacity)]
        self.context["pos"] = list(map(float, self.rect.pos))
        self.context.shader.fs = self.get_shader_string()

    def update_resolution(self) -> None:
        self.context["resolution"] = (*self.rect.size, *self.rect.pos)

    def on_shadow_color(self, instance, value) -> None:
        def on_shadow_color(*args):
            self._shadow_color = list(map(float, value))[:-1] + [
                float(self.opacity) if not self.disabled else 0
            ]
            self.context["shadow_color"] = self._shadow_color

        Clock.schedule_once(on_shadow_color)

    def on_shadow_radius(self, instance, value) -> None:
        def on_shadow_radius(*args):
            if hasattr(self, "context"):
                self.context["shadow_radius"] = list(map(float, value))

        Clock.schedule_once(on_shadow_radius)

    def on_shadow_softness(self, instance, value) -> None:
        def on_shadow_softness(*args):
            if hasattr(self, "context"):
                self.context["shadow_softness"] = float(value)

        Clock.schedule_once(on_shadow_softness)

    def on_elevation(self, instance, value) -> None:
        def on_elevation(*args):
            if hasattr(self, "context"):
                self._elevation = value
                self.hide_elevation(
                    True if (value <= 0 or self.disabled) else False
                )

        Clock.schedule_once(on_elevation)

    def on_shadow_offset(self, instance, value) -> None:
        self.on_size()

    def on_pos(self, *args) -> None:
        if not hasattr(self, "rect"):
            return None

        self.rect.pos = [
            self.widget_pos[0]
            - ((self.rect.size[0] - self.width) / 2)
            - self.shadow_offset[0],
            self.widget_pos[1]
            - ((self.rect.size[1] - self.height) / 2)
            - self.shadow_offset[1],
        ]

        self.context["mouse"] = [self.rect.pos[0], 0.0, 0.0, 0.0]
        self.context["pos"] = list(map(float, self.rect.pos))
        self.update_resolution()

    def on_size(self, *args) -> None:
        if not hasattr(self, "rect"):
            return None

        # If the elevation value is 0, set the canvas size to zero.
        # Because even with a zero elevation value, the shadow is displayed
        # under the widget. This is visible if we change the scale
        # of the widget.
        width = self.size[0] if self.elevation else 0
        height = self.size[1] if self.elevation else 0
        self.rect.size = (
            width
            + (
                self._elevation
                * self.shadow_softness
                / self.shadow_softness_size
            ),
            height
            + (
                self._elevation
                * self.shadow_softness
                / self.shadow_softness_size
            ),
        )

        self.context["mouse"] = [self.rect.pos[0], 0.0, 0.0, 0.0]
        self.context["size"] = list(map(float, self.rect.size))
        self.update_resolution()

    def on_opacity(self, instance, value):
        """
        Adjusts the transparency of the shadow according to the transparency
        of the widget.
        """

        def on_opacity(*args):
            self._shadow_color = list(map(float, self._shadow_color))[:-1] + [
                float(value)
            ]
            self.context["shadow_color"] = self._shadow_color

        super().on_opacity(instance, value)
        Clock.schedule_once(on_opacity)

    def on_radius(self, instance, value) -> None:
        self.shadow_radius = [value[1], value[2], value[0], value[3]]

    def on_disabled(self, instance, value) -> None:
        if value:
            self._elevation = 0
            self.hide_elevation(True)
        else:
            self.hide_elevation(False)

    def hide_elevation(self, hide: bool) -> None:
        if hide:
            self._elevation = -self.elevation
            self._shadow_color = [0.0, 0.0, 0.0, 0.0]
        else:
            self._elevation = self.elevation
            self._shadow_color = self.shadow_color[:-1] + [float(self.opacity)]

        self.on_shadow_color(self, self._shadow_color)
        self.on_size()
        self.on_pos()


class Thumb(CommonElevationBehavior, CircularRippleBehavior, FloatLayout):
    def _set_ellipse(self, instance, value):
        self.ellipse.size = (self._ripple_rad, self._ripple_rad)
        if self.ellipse.size[0] > self.width * 1.5 and not self._fading_out:
            self.fade_out()
        self.ellipse.pos = (
            self.center_x - self._ripple_rad / 2.0,
            self.center_y - self._ripple_rad / 2.0,
        )
        self.stencil.pos = (
            self.center_x - (self.width * self.ripple_scale) / 2,
            self.center_y - (self.height * self.ripple_scale) / 2,
        )
