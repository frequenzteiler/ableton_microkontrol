# emacs-mode: -*- python-*-
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.MixerComponent import MixerComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from EncoderMixerModeSelectorComponent import EncoderMixerModeSelectorComponent
#from RingedEncoderElement import RingedEncoderElement
#from DetailViewControllerComponent import DetailViewControllerComponent
from kmkDetailViewControllerComponent import DetailViewControllerComponent
#from ShiftableDeviceComponent import ShiftableDeviceComponent
from kmkDisplayingDeviceComponent import kmkDisplayingDeviceComponent
from ShiftableTransportComponent import ShiftableTransportComponent
from ShiftableTranslatorComponent import ShiftableTranslatorComponent
from PedaledSessionComponent import PedaledSessionComponent

from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from kmkSysexButtonElement import SysexButtonElement
from kmkSysexLookup import *
device = None


class kmkControlB (ControlSurface):
    __module__ = __name__
    __doc__ = """ Second part of script for Korg Microkontrol by WAC,
    based on the script for Akai's APC40 Controller """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message("!!!!!!!!!!!KMK_B control surface is go!!!!!!!!!!!")
        self.set_suppress_rebuild_requests(True)
        #self._suppress_session_highlight = True
        is_momentary = True
        #self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 98)
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[11])
        #self._suggested_input_port = 'APC40'
        #self._suggested_output_port = 'APC40'
        #session = self._setup_session_control()
        mixer = self._setup_mixer_control()
        self._setup_device_and_transport_control()
        #self._setup_global_control(mixer)
        #session.set_mixer(mixer)
        
        #for component in self._components:
        #    component.set_enabled(False)component.set_enabled

        self.set_suppress_rebuild_requests(False)
        #self._device_id = 0
        #self._common_channel = 0
        #self._dongle_challenge = (Live.Application.get_random_int(0, 2000000),
        # Live.Application.get_random_int(2000001, 4000000))



    def refresh_state(self):
        ControlSurface.refresh_state(self)
        self.schedule_message(5, self._update_hardware)



    def _update_hardware(self):
        #self.set_suppress_rebuild_requests(True)
        #for component in self._components:
        #    component.set_enabled(False)

        #self.set_suppress_rebuild_requests(False)
        #self._suppress_session_highlight = True
        #self._send_midi(SYSEX_INQUIRY)
        self._send_midi(SYSEX_NATIVE_ON)

    """ WAC addition...................................."""
    def handle_sysex(self, midi_bytes):
        if (midi_bytes[0:8] == (SYSEX_KMK_HEADER + (0x5F, 0x03, 0x00))):
            # when native mode transition complete
            self._on_selected_track_changed()
        elif (midi_bytes[0:7] == (SYSEX_KMK_HEADER + (KMK_ENC_COMMAND, 0x08))):
            # toggle lcd displays using 'main' encoder
            device.set_param_name_value_toggle(midi_bytes[7] < 63)
        else:
            # output any sysex received (from KMK_A) back to hardware
            ControlSurface._send_midi(self, midi_bytes)
    """------------------------------------------------"""

# NOT USED IN THIS SCRIPT
#    def _setup_session_control(self):
#        is_momentary = True
#        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 96)
#        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 97)
#        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 94)
#        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 95)
#        session = PedaledSessionComponent(8, 5)
#        session.set_track_bank_buttons(right_button, left_button)
#        session.set_scene_bank_buttons(down_button, up_button)
#        matrix = ButtonMatrixElement()
#        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, (index + 82)) for index in range(5) ]
#        track_stop_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 52) for index in range(8) ]
#        session.set_stop_all_clips_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 81))
#        session.set_stop_track_clip_buttons(tuple(track_stop_buttons))
#        session.set_stop_track_clip_value(2)
#        for scene_index in range(5):
#            scene = session.scene(scene_index)
#            button_row = []
#            scene.set_launch_button(scene_launch_buttons[scene_index])
#            scene.set_triggered_value(2)
#            for track_index in range(8):
#                button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track_index, (scene_index + 53))
#                button_row.append(button)
#                clip_slot = scene.clip_slot(track_index)
#                clip_slot.set_triggered_to_play_value(2)
#                clip_slot.set_triggered_to_record_value(4)
#                clip_slot.set_stopped_value(5)
#                clip_slot.set_started_value(1)
#                clip_slot.set_recording_value(3)
#                clip_slot.set_launch_button(button)
#
#            matrix.add_row(tuple(button_row))
#
#        session.set_slot_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 67))
#        session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 64))
#        session_zoom = SessionZoomingComponent(session)
#        session_zoom.set_button_matrix(matrix)
#        session_zoom.set_zoom_button(self._shift_button)
#        session_zoom.set_nav_buttons(up_button, down_button, left_button, right_button)
#        session_zoom.set_scene_bank_buttons(tuple(scene_launch_buttons))
#        session_zoom.set_stopped_value(3)
#        session_zoom.set_selected_value(5)
#        return session



    def _setup_mixer_control(self):
        is_momentary = True
        #mixer = MixerComponent(8)
        mixer = MixerComponent(1)
        #for track in range(8):
        #    strip = mixer.channel_strip(track)
        #    strip.set_volume_control(SliderElement(MIDI_CC_TYPE, track, 7))
        #    strip.set_arm_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 48))
        #    strip.set_solo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 49))
        #    strip.set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 50))
        #    #strip.set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 51))
        #    strip.set_shift_button(self._shift_button)
        #    strip.set_invert_mute_feedback(True)
        """ WAC addition...................................."""
        mixer.selected_strip().set_mute_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[9]))
        mixer.selected_strip().set_solo_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[13]))
        mixer.set_select_buttons(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[15]),
                                 SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[14]))
        send_faders = []
        NUM_CONTROLLABLE_SENDS = 4
        for index in range(NUM_CONTROLLABLE_SENDS):
            send_faders.append(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[index + 2]))
        mixer.selected_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[0]))
        mixer.selected_strip().set_pan_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[1]))
        mixer.selected_strip().set_send_controls(tuple(send_faders))
        """------------------------------------------------"""
        #mixer.set_crossfader_control(SliderElement(MIDI_CC_TYPE, 0, 15))
        #mixer.set_prehear_volume_control(EncoderElement(MIDI_CC_TYPE, 0, 47, Live.MidiMap.MapMode.relative_two_compliment))
        mixer.set_prehear_volume_control(EncoderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[6], Live.MidiMap.MapMode.absolute))
        #mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, 0, 14))
        mixer.master_strip().set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, KMK_FADER[7]))
        #mixer.master_strip().set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 80))
        return mixer



    def _setup_device_and_transport_control(self):
        is_momentary = True
        device_bank_buttons = []
        device_param_controls = []
        for index in range(8):
            #device_bank_buttons.append(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, (58 + index)))
            device_bank_buttons.append(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[index]))
            #device_param_controls.append(RingedEncoderElement(MIDI_CC_TYPE, 0, (16 + index), Live.MidiMap.MapMode.absolute))
            #device_param_controls[-1].set_ring_mode_button(ButtonElement((not is_momentary), MIDI_CC_TYPE, 0, (24 + index)))
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, 0, KMK_ENCODER[index], Live.MidiMap.MapMode.relative_two_compliment))
            
        #device = ShiftableDeviceComponent()
        global device
        device = kmkDisplayingDeviceComponent() # special component, inherits from ShiftableDeviceController and adds lcds
        device.set_bank_buttons(tuple(device_bank_buttons))
        device.set_shift_button(self._shift_button)
        device.set_parameter_controls(tuple(device_param_controls))
        device.set_on_off_button(device_bank_buttons[1])
        """ WAC addition...................................."""
        device.set_lock_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_PAD[10]))
        parameter_displays = []
        for index in range(8):
            parameter_displays.append(PhysicalDisplayElement(8, 1))
            parameter_displays[-1].set_message_parts((SYSEX_KMK_HEADER + (KMK_LCD_COMMAND, 9, (index + 48))), (247,))
        device_name_display = PhysicalDisplayElement(8,1)
        device_name_display.set_message_parts((SYSEX_KMK_HEADER + (KMK_LCD_COMMAND, 9, (8 + 32))), (247,))
        device.set_display(parameter_displays, device_name_display)
        """------------------------------------------------"""
        self.set_device_component(device)
        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.set_shift_button(self._shift_button)
        detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])
        detail_view_toggler.set_detail_toggle_button(device_bank_buttons[4])
        detail_view_toggler.set_device_nav_buttons(device_bank_buttons[2], device_bank_buttons[3])
        """ WAC addition...................................."""
        detail_view_toggler.set_arrange_toggle_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[8]))
        detail_view_toggler.set_browser_toggle_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, KMK_PAD[12]))
        """------------------------------------------------"""
        transport = ShiftableTransportComponent()
        transport.set_shift_button(self._shift_button)
        #transport.set_play_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 91))
        transport.set_play_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[4]))
        #transport.set_stop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 92))
        transport.set_stop_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[5]))
        #transport.set_record_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 93))
        transport.set_record_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[3]))
        """ WAC addition...................................."""
        transport.set_seek_buttons(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[1]),
                                   SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[0]))
        transport.set_loop_button(SysexButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, KMK_BUTTON[2]))
        """------------------------------------------------"""
        #transport.set_nudge_buttons(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 100), ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 101))
        #transport.set_tap_tempo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 99))
        transport.set_quant_toggle_button(device_bank_buttons[5])
        transport.set_overdub_button(device_bank_buttons[6])
        transport.set_metronome_button(device_bank_buttons[7])
        bank_button_translator = ShiftableTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(device_bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)


# NOT USED IN THIS SCRIPT
#    def _setup_global_control(self, mixer):
#        is_momentary = True
#        global_bank_buttons = []
#        global_param_controls = []
#        for index in range(8):
#            global_param_controls.append(RingedEncoderElement(MIDI_CC_TYPE, 0, (48 + index), Live.MidiMap.MapMode.absolute))
#            global_param_controls[-1].set_ring_mode_button(ButtonElement((not is_momentary), MIDI_CC_TYPE, 0, (56 + index)))
#
#        global_bank_buttons = tuple([ ButtonElement((not is_momentary), MIDI_NOTE_TYPE, 0, (87 + index)) for index in range(4) ])
#        encoder_modes = EncoderMixerModeSelectorComponent(mixer)
#        encoder_modes.set_modes_buttons(global_bank_buttons)
#        encoder_modes.set_controls(tuple(global_param_controls))
#        global_translation_selector = ChannelTranslationSelector()
#        global_translation_selector.set_controls_to_translate(tuple(global_param_controls))
#        global_translation_selector.set_mode_buttons(global_bank_buttons)



    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if ((device_to_select == None) and (len(track.devices) > 0)):
            device_to_select = track.devices[0]
        if (device_to_select != None):
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)



# NOT USED IN THIS SCRIPT
#    def _set_session_highlight(self, track_offset, scene_offset, width, height):
#        if (not self._suppress_session_highlight):
#           ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height)



    """ WAC addition...................................."""
    def update_display(self):
        ControlSurface.update_display(self)
        device.update_display( )



    
    def disconnect(self):                                                      
        self.log_message("--------------= KMK_B Bye Bye =--------------")
        self._send_midi(SYSEX_NATIVE_OFF)
        # call disconnect() method in the base class 
        ControlSurface.disconnect(self)    
        return None
    """------------------------------------------------"""

# local variables:
# tab-width: 4
