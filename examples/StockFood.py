import __init__

from kivygo.app import GoApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

Builder.load_string("""

<RootManager>:
    Screen:
        name: "login"
        GoBoxLayout:
            background_color: GoColors.background_variant_default
            orientation: "vertical"
            GoBoxLayout:
                size_hint_y: None
                height: "250dp"
                GoFloatChild:
                    Image:
                        source: app.get_path("images/Path.png", app._app_file)
                        size_hint: None, None
                        size: list(map(lambda x: x*(root.width/self.texture_size[0]*1.4), self.texture_size))
                        center_x: root.center_x
                        top: root.top + self.height - (dp(250) if self.height >= dp(250) else self.height)
                        mipmap: True
                        fit_mode: "fill"
                GoLabel:
                    text: 'Login'
                    font_size: "50sp"
                    bold: True
                    color: GoColors.on_terciary
                    pos_hint: {"center_y": 0.75}
                GoAnchorLayout:
                    padding: ["0dp", "0dp", "0dp", "60dp"]
                    Image:
                        source: app.get_path("images/6915-green.png", app._app_file)
                        size_hint: None, None
                        size: self.texture_size
                        mipmap: True
                        fit_mode: "fill"
                
            GoAnchorLayout:
                padding: "30dp"
                GoBoxLayout:
                    size_hint_x: None
                    width: min((self.parent.width * 0.7), dp(350))
                    orientation: "vertical"
                    GoInputIcon:
                        label_text: "Name"
                        radius: [dp(5)] * 4
                        text_input_color: GoColors.on_background_variant
                        background_color: GoColors.no_color
                        line_color: GoColors.terciary_border
                        line_color_pos: GoColors.terciary_border_hover
                        label_defaut_color: GoColors.on_background_variant
                        label_pos_color: GoColors.on_background_variant_hover

                    GoAnchorLayout:
                        GoBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            GoInputIcon:
                                label_text: "Password"
                                radius: [dp(5)] * 4
                                text_input_color: GoColors.on_background_variant
                                background_color: GoColors.no_color
                                line_color: GoColors.terciary_border
                                line_color_pos: GoColors.terciary_border_hover
                                label_defaut_color: GoColors.on_background_variant
                                label_pos_color: GoColors.on_background_variant_hover
                            GoLabel:
                                text:'Forget Password?'
                                size_hint_y: None
                                height: self.texture_size[1]
                                text_size: self.width - dp(20), None
                                color: GoColors.on_background_variant
                                halign: "right"
                                font_size: "11sp"
                    
                    GoAnchorLayout:
                        GoButtonRipple:
                            text: "Login"
                            size_hint: None, None
                            size: self.texture_size[0] + dp(100), self.texture_size[1] + dp(30)
                            bold: True
                            font_size: "16sp"
                            radius: [dp(7)] * 4
                            on_release: root.current = "screens_app"
            
            GoAnchorLayout:
                size_hint_y: None
                height: "40dp"
                BoxLayout:
                    size_hint: None, None
                    size: self.minimum_width, "20dp"
                    spacing: "10dp"
                    GoLabel:
                        text: "I don't have an account?"
                        color: GoColors.on_background_variant
                        size_hint_x: None
                        width: self.texture_size[0]
                    GoLabelButton:
                        text: "Register"
                        color: GoColors.on_background_variant
                        size_hint_x: None
                        width: self.texture_size[0]
    Screen:
        name: "screens_app"
        GoBoxLayout:
            orientation: "vertical"
            background_color: GoColors.background_default
            GoBoxLayout:
                size_hint_y: None
                height: "50dp"
                background_color: GoColors.background_variant_default
                GoLabel:
                    text: 'Account'
                    font_size: "22sp"
                    text_size: self.width - dp(20), None
                    bold: True
                    color: GoColors.on_background_variant

            ScreenManager:
                GoSwapScreen:
                    name: "account"
            GoGridLayout:
                size_hint_y: None
                height: "70dp"
                background_color: GoColors.terciary_hover
                cols: 4
                rows: 1
                spacing: "10dp"
                padding: "10dp"
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/python2.svg", app._app_file)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/discord.svg", app._app_file)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/kivy_logo.png", app._app_file)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/facebook2.svg", app._app_file)
""")

class RootManager(ScreenManager):
    pass

class Program(GoApp):
    def build(self):
        self.show_fps = True
        return RootManager()
    

if __name__ == "__main__":
    Program().run()
