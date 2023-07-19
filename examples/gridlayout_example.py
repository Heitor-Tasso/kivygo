import __init__
from kivygo.app import GoApp
from kivygo.layouts.gridlayout import GoDynamicGridLayout
from kivy.lang.builder import Builder


Builder.load_string('''

<MainWidget>:
    pos: root.pos
    size: root.size
    cols: 5
    rows: 2
    spacing: "20dp"
    padding: "10dp"
    GoButton:
        text: "(row: 1, col: 1)"

    GoButton:
        text: "(row: 1, col: 2) \\n colspan: 2  \\n rowspan: 2"
        colspan: 2
        rowspan: 2

    GoButton:
        text: "(row: 1, col: 4) \\n colspan: 2"
        colspan: 2
    GoButton:
        text: "(row: 2, col: 1)"
    GoButton:
        text: "(row: 2, col: 4)"
    GoButton:
        text: "(row: 2, col: 5)"

''')

class MainWidget(GoDynamicGridLayout):
    pass

class TestGridLayoutApp(GoApp):

    def build(self):
        return MainWidget() 
    

if __name__ == "__main__":
    TestGridLayoutApp().run()
