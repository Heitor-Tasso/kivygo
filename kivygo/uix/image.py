
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp

from kivy.uix.widget import Widget
from kivy.uix.image import Image

from kivy.core.image import Image as CoreImage
import tempfile

from svglib import svglib
from reportlab.graphics import renderPM
from reportlab.lib.colors import red, green
from PIL import ImageChops
from PIL import Image as PILImage
import io


def get_kivy_image_from_bytes(image_bytes, file_extension, image_widget=None):
	# Return a Kivy image set from a bytes variable
	buf = io.BytesIO(image_bytes)
	kw = dict()

	if image_widget != None:
		kw = {
			"mipmap": image_widget.mipmap,
			"anim_delay": image_widget.anim_delay,
			"keep_data": image_widget.keep_data,
			"nocache": image_widget.nocache
		}
	cim = CoreImage(buf, ext=file_extension, **kw)
	return cim


def drawing2png(path, fp):
	draw = svglib.svg2rlg(path)
	if draw == None:
		return None
	
	red_img = renderPM.drawToPIL(draw, bg=green, configPIL={'transparent': green})
	green_img = renderPM.drawToPIL(draw, bg=red, configPIL={'transparent': red})
	bg_mask = ImageChops.difference(red_img, green_img).convert('1', dither=PILImage.NONE)
	bg_mask = ImageChops.invert(bg_mask)
	red_img.putalpha(bg_mask)
	red_img.save(fp, fmt='png')


Builder.load_string("""

<RoudedImage>:
	size_hint_x: None
	width: '70dp'
	canvas:
		Color:
			rgba:[1, 1, 1, 1]
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: root.radius
			texture: root.texture


""")


class RoudedImage(Widget):

	texture = ObjectProperty(None)
	source = StringProperty('')
	radius = ListProperty([dp(5), 0, 0, dp(5)])
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.create_texture, 1)

	def create_texture(self, *args):
		image = Image(
			source=self.source, allow_stretch=True, keep_ratio=False, 
			size_hint=(None, None), size=self.size,
		)
		self.texture = image.texture


class ImageWithSVG(Image):
	
	image_source = ObjectProperty('')
	
	def on_image_source(self, *args):

		if isinstance(self.image_source, str):
			self.set_source(self.image_source)

	def set_source(self, source:str):

		if not source.endswith(".svg"):
			self.source = source
			return None
		
		file = tempfile.NamedTemporaryFile(mode='+wb', suffix=".png")
		try:
			drawing2png(source, file)
		except ValueError:
			pass

		file.seek(0)
		img = get_kivy_image_from_bytes(file.read(), 'png', self)
		self.texture = img.texture

