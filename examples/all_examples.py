from __init__ import ExampleAppDefault
from kivy.lang import Builder
from kivygo.layouts.boxlayout import GoBoxLayout
from kivygo.widgets.button import GoButtonRipple
from kivy.uix.scrollview import ScrollView

from anchorlayout_example import AnchorLayoutExample
from tab_example import GoTab, ExampleTab
from anim_bezier_example import AnimBezierExample
from animlabel_example import AnimLabelExample
from bezier_canvas_example import BezierCanvasExample
from boxlayout_example import BoxLayoutExample
from button_example import ButtonExample
from camera_example import CameraExample
from circular_bar_example import CircularBarExample
from circularlayout_example import GoCircularLayout
from datetimepicker_example import GoCircularTimePicker
from drag_example import DragExample
from effect_example import EffectExample
from frostglass_example import FrostGlassExample
from gradient_example import GradientExample
from joystick_example import JoystickExample
from kivg_example import KivgExample
from pipette_example import PipetteExample
from particle_example import ParticleExample
# from slider_example import 
# from taptargetview_example import 
# from rotabox_example import 
# from kivyshadertransitions_example import 
# from progressspinner_example import 
# from radialslider_example import 
# from GoDynamicGridLayout_example import 
# from segment_example import 
# from navigationdrawer_example import 
# from label_gradient_example import 
# from pizzagraph_example import 
# from resize_example import 
# from shader_example import 



Builder.load_string("""

<AllExamples>:
    base_height: "600dp"
    GoBoxLayout:
        orientation: 'vertical'
        spacing: '20dp'
        padding: '20dp'
        size_hint_y: None
        height: self.minimum_height
        background_color: [0.2, 0.4, 0.1, 1]

        PipetteExample:
            size_hint_y: None
            height: root.base_height
	
	    ParticleExample:
            size_hint_y: None
            height: root.base_height
    
        AnchorLayoutExample:
            size_hint_y: None
            height: root.base_height
        
        GoTab:
            size_hint_y: None
            height: root.base_height
            ExampleTab:
                text: "Tab 0"
            ExampleTab:
                text: "Tab 1"

        AnimBezierExample:
            size_hint_y: None
            height: root.base_height

        AnimLabelExample:
            size_hint_y: None
            height: root.base_height

        BezierCanvasExample:
            size_hint_y: None
            height: root.base_height

        GoCircularLayout:
            size_hint_y: None
            height: root.base_height
            direction: "cw"
            start_angle: -75
            inner_radius_hint: 0.7
            padding: "20dp"
            GoButtonRipple:
            GoButtonRipple:
	
        GoCircularTimePicker:
            size_hint_y: None
            height: root.base_height
	
        DragExample:
            size_hint_y: None
            height: root.base_height
	
	    EffectExample:
            size_hint_y: None
            height: root.base_height
	
        FrostGlassExample:
            size_hint_y: None
            height: root.base_height
	    
	    GradientExample:
            size_hint_y: None
            height: root.base_height
	    
	    JoystickExample:
            size_hint_y: None
            height: "700dp"
	        size_hint_x: None
            width: self.parent.width
	    
	    KivgExample:
            size_hint_y: None
            height: root.base_height
	
""")


class AllExamples(ScrollView):
	pass

class AllExamplesApp(ExampleAppDefault):
	def build(self):
		return AllExamples()
	

if __name__ == "__main__":
	AllExamplesApp().run()
