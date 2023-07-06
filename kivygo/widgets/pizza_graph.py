
import math
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


class Pizza(RelativeLayout):
    serie = ListProperty([])
    chart_size = NumericProperty(256)
    legend_color = StringProperty('ffffcc')
    legend_value_rayon = NumericProperty(100)
    legend_title_rayon = NumericProperty(160)
    chart_border = NumericProperty(2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chart_center = self.chart_size / 2.0

        self.bind(
            pos=self.update_pizza,
            size=self.update_pizza,
            serie=self.update_pizza,
            chart_size=self.update_pizza,
            legend_color=self.update_pizza,
            legend_value_rayon=self.update_pizza,
            legend_title_rayon=self.update_pizza,
            chart_border=self.update_pizza
        )
        
        self.bind(
            pos=self.update_label,
            size=self.update_label,
            serie=self.update_label,
            chart_size=self.update_label,
            legend_color=self.update_label,
            legend_value_rayon=self.update_label,
            legend_title_rayon=self.update_label,
            chart_border=self.update_label
        )

    def update_pizza(self, *args):
        with self.canvas:
            self.canvas.clear()
            offset_rotation = 0  # In degrees

            # Fix legend color
            Color(
                get_color_from_hex(self.legend_color)[0],
                get_color_from_hex(self.legend_color)[1],
                get_color_from_hex(self.legend_color)[2], 100
            )

            # Draw pie chart border circle
            border_circle = Line(circle=(
                self.chart_center,
                self.chart_center,
                self.chart_center),
                width=self.chart_border)

            for title, value, color in self.serie:
                angle = math.radians(((value * 3.6) / 2.0) + offset_rotation)
                title_x_pt = (math.sin(angle)) * self.legend_title_rayon
                title_y_pt = (math.cos(angle)) * self.legend_title_rayon

                # Fix color for each zone
                Color(
                    get_color_from_hex(color)[0],
                    get_color_from_hex(color)[1],
                    get_color_from_hex(color)[2], 100
                )

                # Draw zone animation
                zone = Ellipse(
                    size=(self.chart_size, self.chart_size),
                    segments=value * 3.6,
                    angle_start=offset_rotation,
                    angle_end=offset_rotation + (value * 3.6), t='in_quad'
                )

                # Offset control of each zone, drawing starts on offset
                offset_rotation += value * 3.6

    def update_label(self, *args):
        self.clear_widgets()  # Clean widget tree
        offset_rotation = 0  # In degrees

        for title, value, color in self.serie:
            angle = math.radians(((value * 3.6) / 2.0) + offset_rotation)
            value_x_pt = (math.sin(angle)) * self.legend_value_rayon
            value_y_pt = (math.cos(angle)) * self.legend_value_rayon
            title_x_pt = (math.sin(angle)) * self.legend_title_rayon
            title_y_pt = (math.cos(angle)) * self.legend_title_rayon

            # Title
            self.add_widget(Label(
                size_hint=(None, None),
                text="[color=" + self.legend_color + "]" +
                title + "[/color]",
                center_x=self.chart_center + title_x_pt,
                center_y=self.chart_center + title_y_pt,
                markup=True)
            )

            # Value
            self.add_widget(Label(
                size_hint=(None, None),
                text="[color=" + self.legend_color + "]" +
                str(value) + "[/color]",
                center_x=self.chart_center + value_x_pt,
                center_y=self.chart_center + value_y_pt,
                markup=True)
            )

            offset_rotation += value * 3.6
