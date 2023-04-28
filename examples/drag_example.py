import __init__
from kivygo.app import kivygoApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivygo.behaviors.resizable import ResizeSelectBehavior
from kivygo.behaviors.drag_and_drop import DraggableObjectBehavior
from kivygo.uix.boxlayout import DraggableBoxLayout


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex


#:import SpacerWidget kivygo.behaviors.drag_and_drop.SpacerWidget
#:import PreviewWidget kivygo.behaviors.drag_and_drop.PreviewWidget


<ButtonResizable@ResizeSelectBehavior+Button>:

<DragLabel@DraggableObjectBehavior+Label>:


<Manager>:
    
    DraggableBoxLayout:
        drag_classes: ['LABEL_A']
        orientation: 'vertical'
        padding: '5dp'
        spacing: '5dp'
        
        Label:
            text: 'Label-1 | GROUP_A'
        Label:
            text: 'Label-2 | GROUP_A'
        Label:
            text: 'Label-3 | GROUP_A'
    
        DraggableBoxLayout:
            padding: '20dp', 0
            spacing: '5dp'
            drag_classes: ['LABEL_B']
            orientation: 'vertical'
            size_hint_y: 2.5
            
            Label:
                text: 'Label-1 | GROUP_B'
            Label:
                text: 'Label-2 | GROUP_B'
            Label:
                text: 'Label-3 | GROUP_B'
    
    DraggableBoxLayout:
        drag_classes: ['LABEL_A', 'LABEL_B']
        orientation: 'vertical'
        padding: '5dp'
        spacing: '5dp'
        canvas:
            Color:
                rgba: (0, 1, 1, 0.2)
            Rectangle:
                pos: self.pos
                size: self.size
        DragLabel:
            text: 'DRAGABLE_A1'
            drag_cls: 'LABEL_A'
	        preview_widget: PreviewWidget(outline_color=[0, 0, 1, 1])
        DragLabel:
            text: 'DRAGABLE_B1'
            drag_cls: 'LABEL_B'
        DragLabel:
            text: 'DRAGABLE_A2'
            drag_cls: 'LABEL_A'
	        preview_widget: PreviewWidget(outline_color=[0.4, 0, 1, 1], background_color=[0.2, 0.4, 1, 1])
        DragLabel:
            text: 'DRAGABLE_B2'
            drag_cls: 'LABEL_B'
        DragLabel:
            text: 'DRAGABLE_A3'
            drag_cls: 'LABEL_A'
        DragLabel:
            text: 'DRAGABLE_B3'
            drag_cls: 'LABEL_B'
        DragLabel:
            text: 'DRAGABLE_A4'
            drag_cls: 'LABEL_A'

""")


class Manager(BoxLayout):
	pass

class ExampleUixApp(kivygoApp):
	def build(self):
		return Manager()
	

if __name__ == "__main__":
	ExampleUixApp().run()

