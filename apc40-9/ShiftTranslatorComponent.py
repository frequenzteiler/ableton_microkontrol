# Source Generated with Decompyle++
# File: ShiftTranslatorComponent.pyc (Python 2.5)

from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from _Framework.ButtonElement import ButtonElement
from _Framework.MixerComponent import MixerComponent

class ShiftTranslatorComponent(ChannelTranslationSelector):
    ''' Class that translates the channel of some buttons as long as a shift button is held '''
    
    def __init__(self):
        ChannelTranslationSelector.__init__(self)
        self._shift_button = None
        self._shift_pressed = False

    
    def disconnect(self):
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        
        ChannelTranslationSelector.disconnect(self)

    
    def set_shift_button(self, button):
        if not button == None:
            if not isinstance(button, ButtonElement) or button.is_momentary():
                raise AssertionError
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
        
        self._shift_button = button
        if self._shift_button != None:
            self._shift_button.add_value_listener(self._shift_value)
        
        self.set_mode(0)

    
    def on_enabled_changed(self):
        if self.is_enabled():
            self.set_mode(int(self._shift_pressed))
        

    
    def number_of_modes(self):
        return 2

    
    def _shift_value(self, value):
        if not self._shift_button != None:
            raise AssertionError
        if not value in range(128):
            raise AssertionError
        self._shift_pressed = value != 0
        if self.is_enabled():
            self.set_mode(int(self._shift_pressed))
        


