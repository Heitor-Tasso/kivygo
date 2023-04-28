
from kivy.lang import global_idmap
from kivy.properties import (
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.effectwidget import AdvancedEffectBase, EffectWidget
from kivy.graphics import BindTexture

GLSL = """

uniform sampler2D mask;
uniform vec2 mask_pos;
uniform vec2 mask_size;

// 0: the mask pixel multiply the texture
// 1: the mask pixel substract to the texture
// addition and division don't seem to be of any use
uniform int mode;
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords){
    // get the pixel lookup pos in the mask relative to our main texture
    vec2 pos = tex_coords; // - mask_pos * resolution;
    vec2 size = mask_size / resolution;
    if (
        pos.x < 0. || pos.y < 0. ||
        pos.x > 1. || pos.y > 1.
    )
        if (mode == 0)
            return vec4(0.);
        else
            return color;
    if (mode == 0)
        return color * texture2D(mask, pos);
    else
        return color - texture2D(mask, pos);
}
"""


class MaskEffect(AdvancedEffectBase):
    mask = ObjectProperty(None)
    glsl = StringProperty(GLSL)
    mode = OptionProperty("multiply", options=["multiply", "substract"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        assert self.mask
        self.mask.bind(
            pos=self.update_mask,
            size=self.update_mask,
        )
        self.bind(mode=self.update_mask)

    def on_fbo(self, *args):
        self.update_mask()

    def update_mask(self, *args):
        with self.fbo:
            BindTexture(texture=self.mask.fbo.texture, index=1)
        
        self.uniforms.update(
            {
                "mask": 1,
                "mask_pos": list(self.mask.pos),
                "mask_size": list(self.mask.size),
                "mode": 0 if self.mode == "multiply" else 1,
            }
        )


global_idmap["MaskEffect"] = MaskEffect
