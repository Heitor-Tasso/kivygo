from __init__ import ExampleAppDefault
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

Builder.load_string("""

#:import Light kivygo.colors.Light
#:import Dark kivygo.colors.Dark

<RootManager>:
    Screen:
        name: "login"
        GoBoxLayout:
            background_color: GoColors.background_default
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
                    color: GoColors.at_terciary_default
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
                        text_input_color: GoColors.at_background_default
                        background_color: GoColors.no_color
                        line_color: GoColors.terciary_border
                        label_defaut_color: GoColors.at_background_default
                        label_pos_color: GoColors.at_background_hover

                    GoAnchorLayout:
                        GoBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            GoInputIcon:
                                label_text: "Password"
                                radius: [dp(5)] * 4
                                text_input_color: GoColors.at_background_default
                                background_color: GoColors.no_color
                                line_color: GoColors.terciary_border
                                label_defaut_color: GoColors.at_background_default
                                label_pos_color: GoColors.at_background_hover
                            GoLabelButton:
                                text:'Forget Password?'
                                size_hint_y: None
                                height: self.texture_size[1]
                                text_size: self.width - dp(20), None
                                normal_color: GoColors.at_background_default
                                down_color: GoColors.at_background_pressed
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
                        color: GoColors.at_background_default
                        size_hint_x: None
                        width: self.texture_size[0]
                    GoLabelButton:
                        text: "Register"
                        normal_color: GoColors.at_background_default
                        down_color: GoColors.at_background_pressed
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
                background_color: GoColors.background_default
                GoLabel:
                    text: 'Account'
                    font_size: "22sp"
                    text_size: self.width - dp(20), None
                    bold: True
                    color: GoColors.at_background_default

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
                        on_release: GoColors.palette = (Light if GoColors.palette == Dark else Dark)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/discord.svg", app._app_file)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/kivy_logo.png", app._app_file)
                GoAnchorLayout:
                    GoIconButton:
                        source: app.get_path("icons/facebook2.svg", app._app_file)
                        on_release: root.current = "login"
""")

class RootManager(ScreenManager):
    pass

class Program(ExampleAppDefault):
    def build(self):
        return RootManager()
    

if __name__ == "__main__":
    Program().run()
