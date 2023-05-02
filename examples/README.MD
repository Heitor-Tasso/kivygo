# KivyGO UIX DOC
---

## `kivygo/uix/anchorlayout.py`
### AnchorLayout

Layout que permite ancorar um widget em qualquer um dos quatro cantos ou no centro. Os widgets filhos são esticados para preencher todo o espaço restante.
<img align="right" width="300" height="500" src="../images_example/example_2.gif"/>

<details>
<summary>AnchorLayout Centered</summary>
<ul>
<img align="right" width="400" height="400" src="../images_example/example_2.gif"/>

```python
GridLayout:
    size_hint_y: None
    height: self.minimum_height

    canvas:
        Color:
            rgba: app.theme_cls.primary_color
        Rectangle:
            pos: self.pos
            size: self.size
```
</ul>
</details>

|[Click here](https://github.com/)|
|---|


---
