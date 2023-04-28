import __init__
from kivy.app import App
from kivygo.uix.pizza_graph import Pizza


class ChartApp(App):
        """
        Example application

        """
        def build(self):
            from kivy.uix.gridlayout import GridLayout
            from kivy.uix.slider import Slider
            import random

            def test(*args):
                lang_pizza.legend_value_rayon = slider_ray.value
                fruit_pizza.legend_value_rayon = slider_ray.value

            def rand(*args):
                lang = ["Français", "Belge", "Anglais", "Allemand", "Italien"]
                value = [25, 10, 15, 30, 20]
                color = ['a9a9a9', '808080', '696969', '778899', '708090']
                random.shuffle(lang)
                random.shuffle(value)
                random.shuffle(color)
                lang_pizza.serie = zip(lang, value, color)

            layout = GridLayout(cols=2, padding=50)
            lang_pizza = Pizza(serie=[
                ["Français", 5, 'a9a9a9'],
                ["Belge", 25, '808080'],
                ["Anglais", 20, '696969'],
                ["Allemand", 30, '778899'],
                ["Italien", 20, '708090']],
                chart_size=256,
                legend_color='ffffcc',
                legend_value_rayon=100,
                legend_title_rayon=170,
                chart_border=2)

            fruit_pizza = Pizza(serie=[
                ["Pomme", 20, '6495ed'],
                ["Poire", 20, '7b68ee'],
                ["Abricot", 20, '4169e1'],
                ["Prune", 20, '0000ff'],
                ["Ananas", 20, '00008b']],
                chart_size=256,
                legend_color='ffffcc',
                legend_value_rayon=100,
                legend_title_rayon=170,
                chart_border=2)

            slider_v = Slider(min=0, max=300, value=50)
            slider_v.bind(value=rand)

            slider_ray = Slider(min=0, max=250, value=100)
            slider_ray.bind(value=test)

            layout.add_widget(lang_pizza)
            layout.add_widget(fruit_pizza)
            layout.add_widget(slider_v)
            layout.add_widget(slider_ray)

            return layout

if __name__ == '__main__':
    ChartApp().run()
