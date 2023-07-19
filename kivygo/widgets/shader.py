
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import (
    RenderContext, Fbo, Color,
    ClearColor, ClearBuffers,
    Rectangle
)
from kivygo.layouts.floatlayout import GoFloatLayout
from kivy.properties import (
    StringProperty, ListProperty,
    ObjectProperty
)


header = '''

$HEADER$
uniform vec2 resolution;
uniform float time;
uniform vec2 mouse;

'''


shader_watter_bubble = (header + '''

void main(void)
{
	vec2 halfres = resolution.xy / 2.0;
	vec2 cpos = vec4(frag_modelview_mat * gl_FragCoord).xy;

	vec2 sinres = vec2(tan(resolution.x * time), -sin(resolution * time));

	cpos.x -= 0.5 * halfres.x * sin(time/2.0) + \
		0.3 * halfres.x * cos(time) + halfres.x;

	cpos.y -= 0.5 * halfres.y * sin(time/5.0) + \
		0.3 * halfres.y * sin(time) + halfres.y;

	float cLength = length(cpos);

	vec2 uv = \
		tex_coord0 + (cpos / cLength) * \
			sin(cLength / 50.0 - time * 2.0) / 15.0;

	vec3 col = texture2D(texture0, uv).xyz;
	gl_FragColor = vec4(col, 1.0);
}

''')




class GoShaderWidget(GoFloatLayout):

    mouse_pos = ListProperty([100, 100])

    fs = StringProperty(None)

    texture = ObjectProperty(None)

    def __init__(self, **kwargs):

        Window.bind(mouse_pos=self.get_mouse_pos)

        self.canvas = RenderContext(
            use_parent_projection=True,
            use_parent_modelview=True,
            use_parent_frag_modelview=True
        )

        with self.canvas:
            self.fbo = Fbo(size=self.size)
            self.fbo_color = Color(1, 1, 1, 1)
            self.fbo_rect = Rectangle(size=self.size, pos=self.pos)

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()

        super().__init__(**kwargs)

        self.fs = shader_watter_bubble
        Clock.schedule_interval(self.update_glsl, 0)

    def get_mouse_pos(self, w, pos):
        self.canvas['mouse'] = pos
        self.mouse_pos = pos

    def update_glsl(self, *largs):
        self.canvas['time'] = Clock.get_boottime()
        self.canvas['resolution'] = [float(v) for v in self.size]

    def on_fs(self, instance, value):

        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception('compilation failed')

    def add_widget(self, *args, **kwargs):
        c = self.canvas
        self.canvas = self.fbo
        super().add_widget(*args, **kwargs)
        self.canvas = c

    def remove_widget(self, *args, **kwargs):
        c = self.canvas
        self.canvas = self.fbo
        super().remove_widget(*args, **kwargs)
        self.canvas = c

    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value


