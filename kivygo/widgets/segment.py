
from kivy.properties import StringProperty, BoundedNumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Ellipse, Mesh, Scale
from kivy.utils import get_color_from_hex


class GoSegment(RelativeLayout):
  
    scale = BoundedNumericProperty(0.1, min=0.1, max=1, errorvalue=0.2)
    color = StringProperty('2fc827')
    value = StringProperty('A.')

    def __init__(self, **kwargs):     
        super().__init__(**kwargs)

        # Drawing meshes configuration, indices range meshes and mode
        self.indice = range(0, 6)
        self.xmode = 'triangle_fan'
        
        # GoSegment matrix configuration
        seg_1 = [
            20, 215, 0, 0,
            35, 230, 0, 0,
            95, 230, 0, 0,
            110, 215, 0, 0,
            95, 200, 0, 0,
            35, 200, 0, 0,
        ]
        seg_2 = [
            15, 210, 0, 0,
            30, 195, 0, 0,
            30, 135, 0, 0,
            15, 120, 0, 0,
            0, 135, 0, 0,
            0, 195, 0, 0,
        ]
        seg_3 = [
            115, 210, 0, 0,
            130, 195, 0, 0,
            130, 135, 0, 0,
            115, 120, 0, 0,
            100, 135, 0, 0,
            100, 195, 0, 0,
        ]
        seg_4 = [
            20, 115, 0, 0,
            35, 130, 0, 0,
            95, 130, 0, 0,
            110, 115, 0, 0,
            95, 100, 0, 0,
            35, 100, 0, 0,
        ]
        seg_5 = [
            15, 110, 0, 0,
            30, 95, 0, 0,
            30, 35, 0, 0,
            15, 20, 0, 0,
            0, 35, 0, 0,
            0, 95, 0, 0,
        ]
        seg_6 = [
            115, 110, 0, 0,
            130, 95, 0, 0,
            130, 35, 0, 0,
            115, 20, 0, 0,
            100, 35, 0, 0,
            100, 95, 0, 0,
        ]
        seg_7 = [
            20, 15, 0, 0,
            35, 30, 0, 0,
            95, 30, 0, 0,
            110, 15, 0, 0,
            95, 0, 0, 0,
            35, 0, 0, 0,
        ]

        # Drawing association
        type_0 = [seg_1, seg_2, seg_3, seg_5, seg_6, seg_7]
        type_1 = [seg_3, seg_6]
        type_2 = [seg_1, seg_3, seg_4, seg_5, seg_7]
        type_3 = [seg_1, seg_3, seg_4, seg_6, seg_7]
        type_4 = [seg_2, seg_3, seg_4, seg_6]
        type_5 = [seg_1, seg_2, seg_4, seg_6, seg_7]
        type_6 = [seg_1, seg_2, seg_4, seg_5, seg_6, seg_7]
        type_7 = [seg_1, seg_3, seg_6]
        type_8 = [seg_1, seg_2, seg_3, seg_4, seg_5, seg_6, seg_7]
        type_9 = [seg_1, seg_2, seg_3, seg_4, seg_6, seg_7]
        type_A = [seg_1, seg_2, seg_3, seg_4, seg_5, seg_6]
        type_b = [seg_2, seg_4, seg_5, seg_6, seg_7]
        type_C = [seg_1, seg_2, seg_5, seg_7]
        type_d = [seg_3, seg_4, seg_5, seg_6, seg_7]
        type_E = [seg_1, seg_2, seg_4, seg_5, seg_7]
        type_F = [seg_1, seg_2, seg_4, seg_5]

        # Routing association
        self.type_dic = {
                "0" : type_0,
                "0.": type_0,
                "1" : type_1,
                "1.": type_1,
                "2" : type_2,
                "2.": type_2,
                "3" : type_3,
                "3.": type_3,
                "4" : type_4,
                "4.": type_4,
                "5" : type_5,
                "5.": type_5,
                "6" : type_6,
                "6.": type_6,
                "7" : type_7,
                "7.": type_7,
                "8" : type_8,
                "8.": type_8,
                "9" : type_9,
                "9.": type_9,
                "A" : type_A,
                "A.": type_A,
                "b" : type_b,
                "b.": type_b,
                "C" : type_C,
                "C.": type_C,
                "d" : type_d,
                "d.": type_d,
                "E" : type_E,
                "E.": type_E,
                "F" : type_F,
                "F.": type_F,
                }

        # Binding refresh drawing method
        self.bind(
            pos=self._update_canvas, 
            size=self._update_canvas,
            value=self._update_canvas
            )

    def _update_canvas(self, *args):

        with self.canvas:

            # Refresh
            self.canvas.clear()

            # Configure
            Color(
                get_color_from_hex(self.color)[0], 
                get_color_from_hex(self.color)[1], 
                get_color_from_hex(self.color)[2], 100
            )

            Scale(self.scale)

            def make_mesh(self, ttype, *args):
                for segment in ttype:
                    Mesh(
                        vertices=segment, 
                        indices=self.indice, 
                        mode=self.xmode
                        )
                if len(self.value) > 1:
                    Ellipse(pos=(135, 0), size=(25,25), segments=360)

            # Avoid if session
            for key, val in self.type_dic.items():
                if self.value == key:
                    make_mesh(self, ttype=val)
      
