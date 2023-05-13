

from kivy.compat import string_types
from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivygo.uix.button import ButtonEffect
from kivy.uix.dropdown import DropDown


class EffectSpinner(ButtonEffect):

    values = ListProperty([])
    '''Values that can be selected by the user. It must be a list of strings.
    '''

    text_autoupdate = BooleanProperty(False)
    '''Indicates if the spinner's :attr:`text` should be automatically
    updated with the first value of the :attr:`values` property.
    Setting it to True will cause the spinner to update its :attr:`text`
    property every time attr:`values` are changed.
    '''

    option_cls = ObjectProperty(ButtonEffect)
    '''Class used to display the options within the dropdown list displayed
    under the Spinner. The `text` property of the class will be used to
    represent the value.

    The option class requires:

    - a `text` property, used to display the value.
    - an `on_release` event, used to trigger the option when pressed/touched.
    - a :attr:`~kivy.uix.widget.Widget.size_hint_y` of None.
    - the :attr:`~kivy.uix.widget.Widget.height` to be set.
    '''

    dropdown_cls = ObjectProperty(DropDown)
    '''Class used to display the dropdown list when the Spinner is pressed.
    '''

    is_open = BooleanProperty(False)
    '''By default, the spinner is not open. Set to True to open it.
    '''

    sync_height = BooleanProperty(True)
    '''Each element in a dropdown list uses a default/user-supplied height.
    Set to True to propagate the Spinner's height value to each dropdown
    list element.
    '''

    def __init__(self, **kwargs):
        self._dropdown = None
        super().__init__(**kwargs)
        fbind = self.fbind
        build_dropdown = self._build_dropdown
        fbind('on_release', self._toggle_dropdown)
        fbind('dropdown_cls', build_dropdown)
        fbind('option_cls', build_dropdown)
        fbind('values', self._update_dropdown)
        fbind('size', self._update_dropdown_size)
        fbind('text_autoupdate', self._update_dropdown)
        build_dropdown()

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.unbind(on_select=self._on_dropdown_select)
            self._dropdown.unbind(on_dismiss=self._close_dropdown)
            self._dropdown.dismiss()
            self._dropdown = None

        cls = self.dropdown_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._dropdown = cls()
        self._dropdown.bind(on_select=self._on_dropdown_select)
        self._dropdown.bind(on_dismiss=self._close_dropdown)
        self._update_dropdown()

    def _update_dropdown_size(self, *largs):
        
        if not self.sync_height or not self._dropdown:
            return None

        container = self._dropdown.container
        if not container:
            return None
        
        h = self.height
        for item in container.children[:]:
            item.height = h

    def _update_dropdown(self, *largs):
        cls = self.option_cls
        values = self.values
        text_autoupdate = self.text_autoupdate
        if isinstance(cls, string_types):
            cls = Factory.get(cls)

        self._dropdown.clear_widgets()
        for value in values:
            item = cls(text=value, size_hint_y=None)
            item.height = self.height if self.sync_height else item.height
            item.bind(on_release=lambda option: self._dropdown.select(option.text))
            self._dropdown.add_widget(item)
        
        if text_autoupdate:
            if values:
                if not self.text or self.text not in values:
                    self.text = values[0]
            else:
                self.text = ''

    def _toggle_dropdown(self, *largs):
        if self.values:
            self.is_open = True

    def _close_dropdown(self, *largs):
        self.is_open = False

    def _on_dropdown_select(self, instance, data, *largs):
        self.text = data
        self.is_open = False

    def on_is_open(self, instance, value):
        if value:
                self._dropdown.open(self)
        else:
            self._dropdown.dismiss()
