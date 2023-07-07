
__version__ = "0.0.4"

from kivy.factory import Factory

def load_factory():
    classes = {
        "widgets" : [
            { "button": ["GoButton", "GoRippleButton", "GoRippleToggleButton", "GoFadeButton", "GoFadeToggleButton"] },
            { "widget": ["GoWidget", "ShaderWidget"] },
            { "slider": ["NeuSlider", "NeuThumb"] }
        ],
        "layouts" : [
            { "boxlayout": ["GoBoxLayoutColor", "GoDraggableBoxLayout"] },
            { "anchorlayout": ["GoAnchorLayoutColor"] }
        ],
        "behaviors" : [
            { "button": ["ButtonBehavior", "ToggleButtonBehavior"] },
            { "hover": ["HoverBehavior"] }
        ],
    }
    for key, item in classes.items():
        for obj in item:
            if isinstance(obj, dict):
                md = list(obj.keys())[0]
                for name_class in list(obj.values())[0]:
                    Factory.register(name_class, module=f"kivygo.{key}.{md}")
            else:
                for name_class in item:
                    Factory.register(name_class, module=f"kivygo.{key}")

load_factory()
