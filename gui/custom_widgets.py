
from abc import ABC, abstractmethod

class ModifiedTextMixin(ABC):
    """
    This class provides on_ui_modify on_modify methods to overwrite.
    Overwritining those methods allows to catch Text Widget modification
    """
    def __init__(self):
        self.is_changing = False
        self.bind('<<Modified>>', self.__handle_on_modify)

    def __handle_on_modify(self, *args, **kwargs):
        if self.edit_modified() and not self.is_changing:
            self.is_changing = True
            self.on_ui_modify()
            self.edit_modified(0)
            self.is_changing = False
        self.on_modify()

    @abstractmethod
    def on_ui_modify(self):
        """Ovewrite this class to define action for modification of Text Widged only on UI side."""
        pass

    @abstractmethod
    def on_modify(self):
        """Ovewrite this class to define action for every Text Widged modification
        (including progrmaming e.g: text.insert etc)"""
        pass







