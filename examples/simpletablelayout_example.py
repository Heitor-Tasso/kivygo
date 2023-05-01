import __init__
from kivygo.app import kivygoApp
from kivygo.uix.simpletablelayout import SimpleTableLayout
from kivy.lang.builder import Builder


Builder.load_string('''

<MainWidget>:
    pos: root.pos
    size: root.size
    cols: 5
    rows: 2

    Button:
        text: "(row: 1, col: 1)"

    Button:
        text: "(row: 1, col: 2) \\n colspan: 2  \\n rowspan: 2"
        colspan: 2
        rowspan: 2

    Button:
        text: "(row: 1, col: 4) \\n colspan: 2"
        colspan: 2
    Button:
        text: "(row: 2, col: 1)"
    Button:
        text: "(row: 2, col: 4)"
    Button:
        text: "(row: 2, col: 5)"

''')

class MainWidget(SimpleTableLayout):
    pass

class TestSimpleTableApp(kivygoApp):

    def build(self):
        return MainWidget() 
    

if __name__ == "__main__":
    TestSimpleTableApp().run()
