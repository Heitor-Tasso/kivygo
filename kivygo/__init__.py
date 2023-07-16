
__version__ = "0.0.4"

from kivygo.app import GoApp
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.clock import Clock


Builder.load_string("""

#:import Colors kivygo.colors.Colors

#:set GoColors Colors()

""")


def load_factory():
	classes = {
		"widgets" : [
			{ "button": ["GoButton", "GoButtonRipple", "GoToggleButtonRipple", "GoButtonFade", "GoToggleButtonFade"] },
			{ "widget": ["GoWidget", "ShaderWidget"] },
			{ "slider": ["NeuSlider", "NeuThumb"] },
			{ "input": ["GoInputIcon", ] },
			{ "screenmanager": ["GoSwapScreen", ] },
			{ "label": ["GoLabel", "GoLabelButton", "GoLabelGradient", "GoLabelScroll", "GoLabelAnimated", "GoLabelBezierAnimated"] },
			{ "image": ["GoImage", ] },
			{ "icon": ["GoIcon", "GoIconButton", "GoIconButtonRipple", "GoIconButtonFade", "GoIconToggleButton", "GoIconToggleButtonRipple", "GoIconToggleButtonFade"] }
		],
		"layouts" : [
			{ "boxlayout": ["GoBoxLayout", "GoBoxLayoutColor", "GoDraggableBoxLayout"] },
			{ "anchorlayout": ["GoAnchorLayout", "GoAnchorLayoutColor"] },
			{ "gridlayout": ["GoGridLayout", "GoGridLayoutColor", "DynamicGridLayout"] }
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


__clock = Builder.load_string("""

GoBoxLayout:
	size_hint: None, None
	height: "15dp"
	padding: ["30dp", "0dp", "0dp", "0dp"]
	background_color: GoColors.primary_default
	Label:
		id: clock_label
		default_text: "Current: {:.2f}  |  Min: {:.2f}  |  Max: {:.2f}"
		text_size: self.width, None
		halign: "left"
		color: GoColors.on_primary
		font_size: '12sp'
		bold: True
""")

_min_fps = None
_max_fps = None

def update_clock(*args):
	global _min_fps, _max_fps

	_app = GoApp.get_running_app()
	if _app == None:
		return None
	
	lbl = __clock.ids.clock_label
	fps = Clock.get_fps()
	
	_min_fps = min(_min_fps, fps) if _min_fps != None else fps
	_max_fps = max(_max_fps, fps) if _max_fps != None else fps

	lbl.text = lbl.default_text.format(fps, _min_fps, _max_fps)
	__clock.width = _app.root.width
	__clock.pos = [_app.root.x, _app.root.top - __clock.height]

	if _min_fps == 0:
		_min_fps = None

def check_app(*args):
	app = GoApp.get_running_app()
	if app == None:
		return None
	
	if not app.show_fps:
		return Clock.unschedule(check_app)
	
	app.root.padding = 70
	Clock.unschedule(check_app)

	win = app.root.get_root_window()
	win.add_widget(__clock)
	Clock.schedule_interval(update_clock, 0.01)

Clock.schedule_interval(check_app, 0.1)
