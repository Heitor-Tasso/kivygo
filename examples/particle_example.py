from __init__ import ExampleAppDefault
from kivy.uix.gridlayout import GridLayout
from kivygo.widgets.widget import GoWidget
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivygo.widgets.particle import GoParticleSystem

Builder.load_string("""

<ParticleExample>:
    cols: 2

    DemoParticle:
        id: paint
    
    BoxLayout:
        orientation: "vertical"
        size_hint_x: None
        width: "70dp"

        GoButtonRipple:
            text: 'Sun'
            on_press: paint.show_sun()
        
        GoButtonRipple:
            text: 'Drugs'
            on_press: paint.show_drugs()
        
        GoButtonRipple:
            text: 'JellyFish'
            on_press: paint.show_jellyfish()
        
        GoButtonRipple:
            text: 'Fire'
            on_press: paint.show_fire()

""")

class DemoParticle(GoWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.can_draw = False
        self.sun = GoParticleSystem('kivygo/config/sun.pex')
        self.drugs = GoParticleSystem('kivygo/config/drugs.pex')
        self.jellyfish = GoParticleSystem('kivygo/config/jellyfish.pex')
        self.fire = GoParticleSystem('kivygo/config/fire.pex')

        self.current = None
        Clock.schedule_once(self.config)
    
    def config(self, *args):
        self._show(self.sun)

    def on_touch_down(self, touch):
        self.can_draw = False
        if not self.current:
            return None
        
        if not self.collide_point(*touch.pos):
            return False
        
        self.can_draw = True
        self.current.emitter_x = float(touch.x)
        self.current.emitter_y = float(touch.y)

    def on_touch_move(self, touch):
        if not self.current or not self.can_draw:
            return None
        
        self.current.emitter_x = float(touch.x)
        self.current.emitter_y = float(touch.y)

    def show_sun(self, *args):
        self._show(self.sun)

    def show_drugs(self, *args):
        self._show(self.drugs)

    def show_jellyfish(self, *args):
        self._show(self.jellyfish)

    def show_fire(self, *args):
        self._show(self.fire)

    def _show(self, system):
        if system == None:
            return None
        
        if self.current:
            if self.current is not system:
                self.remove_widget(self.current)
                self.current.stop(True)
        self.current = system

        self.current.emitter_x = self.center_x
        self.current.emitter_y = self.center_y
        if self.current is not system or not self.children:
            self.add_widget(self.current)
            self.current.start()
    
    def on_pos(self, *args):
        self._show(self.current)
    
    def on_size(self, *args):
        self._show(self.current)


class ParticleExample(GridLayout):
    pass

class ParticleExampleApp(ExampleAppDefault):
    def build(self):
        return ParticleExample()


if __name__ == '__main__':
    ParticleExampleApp().run()
