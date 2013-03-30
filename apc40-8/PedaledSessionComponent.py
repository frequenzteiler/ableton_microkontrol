# Source Generated with Decompyle++
# File: PedaledSessionComponent.pyc (Python 2.5)

import Live
from APCSessionComponent import APCSessionComponent
from _Framework.ButtonElement import ButtonElement

class PedaledSessionComponent(APCSessionComponent):
    ''' Special SessionComponent with a button (pedal) to fire the selected clip slot '''
    
    def __init__(self, num_tracks, num_scenes):
        APCSessionComponent.__init__(self, num_tracks, num_scenes)
        self._slot_launch_button = None

    
    def disconnect(self):
        APCSessionComponent.disconnect(self)
        if self._slot_launch_button != None:
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None
        

    
    def set_slot_launch_button(self, button):
        if not button == None and isinstance(button, ButtonElement):
            raise AssertionError
        if self._slot_launch_button != button:
            if self._slot_launch_button != None:
                self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            
            self._slot_launch_button = button
            if self._slot_launch_button != None:
                self._slot_launch_button.add_value_listener(self._slot_launch_value)
            
            self.update()
        

    
    def _slot_launch_value(self, value):
        if not value in range(128):
            raise AssertionError
        if not self._slot_launch_button != None:
            raise AssertionError
        if self.is_enabled():
            if value != 0 or not self._slot_launch_button.is_momentary():
                if self.song().view.highlighted_clip_slot != None:
                    self.song().view.highlighted_clip_slot.fire()
                
            
        


