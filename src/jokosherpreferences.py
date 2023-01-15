from gi.repository import Adw, Gtk, Gio

class JokosherPreferences(Adw.PreferencesWindow):
    def __init__(self):
        Adw.PreferencesWindow.__init__(self)

        self.general_options = Adw.PreferencesPage.new()
        self.general_options.set_name("GeneralOptions")
        self.general_options.set_title("General Options")
        self.general_options.set_icon_name("window-new")
        self.add(self.general_options)

        self.first_page_behavior_options = Adw.PreferencesGroup.new()
        self.first_page_behavior_options.set_description("Options to change application behavior")
        self.first_page_behavior_options.set_title("Behavior Options")
        self.general_options.add(self.first_page_behavior_options)

        self.project_dialog_show_action = Adw.ActionRow.new()
        self.project_dialog_show_action.set_title("Show project dialog")
        self.project_dialog_show_action.set_subtitle("Whatever show project dialog when opening application")
        self.project_dialog_show_action_switch = Gtk.Switch()
        self.project_dialog_show_action.add_suffix(self.project_dialog_show_action_switch)
        self.project_dialog_show_action.set_activatable_widget(self.project_dialog_show_action_switch)
        self.project_dialog_show_action_switch.props.vexpand = False
        self.project_dialog_show_action_switch.props.valign = Gtk.Align.CENTER

        self.first_page_behavior_options.add(self.project_dialog_show_action)

        self.settings = Gio.Settings("org.gnome.Jokosher")
        self.settings.bind('show-project-dialog', self.project_dialog_show_action_switch, 'active', Gio.SettingsBindFlags.DEFAULT)

        self.audio_preferences = Adw.PreferencesPage.new()
        self.audio_preferences.set_name("AudioPreferences")
        self.audio_preferences.set_title("Audio Preferences")
        self.audio_preferences.set_icon_name("audio-card")
        self.add(self.audio_preferences)

        self.audio_preferences_system_devices = Adw.PreferencesGroup.new()
        self.audio_preferences_system_devices.set_description("Choose audio system and devices")
        self.audio_preferences_system_devices.set_title("Audio System And Devices")
        self.audio_preferences.add(self.audio_preferences_system_devices)

        self.audio_system_select_action = Adw.ComboRow.new()
        self.audio_system_select_action.set_title("Audio System")
        self.audio_system_select_action.set_subtitle("Which audio system to use for playback and recording")
        self.audio_system_select_action.set_model(Gtk.StringList.new(['Automatic', 'Pulse Audio', 'JACK']))
        self.audio_system_select_action.set_selected(self.settings.get_value('audio-system').unpack())
        self.audio_preferences_system_devices.add(self.audio_system_select_action)

        #settings.bind_with_mapping('audio-system', self.audio_system_select_action, 'selected-item', Gio.SettingsBindFlags.DEFAULT, self.get_audio_system_select, self.set_audio_system_select)
        #settings.bind('audio-system', self.audio_system_select_action, 'selected', Gio.SettingsBindFlags.DEFAULT)
        self.audio_system_select_action.connect("notify::selected", self.on_audio_system_selected)
        self.audio_default_settings = Adw.PreferencesGroup.new()
        self.audio_default_settings.set_description("Default audio settings for new project to use")
        self.audio_default_settings.set_title("Default Audio Settings")
        self.audio_preferences.add(self.audio_default_settings)

        self.default_recording_format = Adw.ComboRow.new()
        self.default_recording_format.set_title("Recording Format")
        self.default_recording_format.set_subtitle("Which codec format to use for recording and/or importing audio")
        self.default_recording_format.set_model(Gtk.StringList.new(['FLAC', 'WAV']));
        self.audio_default_settings.add(self.default_recording_format)

        self.default_sample_rate = Adw.ComboRow.new()
        self.default_sample_rate.set_title("Audio sample rate")
        self.default_sample_rate.set_subtitle("Number of samples taken per second to store audio digitally")
        self.default_sample_rate.set_model(Gtk.StringList.new(['44.1Hz', '48Hz', '96Hz']));
        self.audio_default_settings.add(self.default_sample_rate)

        self.default_bit_rate = Adw.ComboRow.new()
        self.default_bit_rate.set_title("Audio bit rate")
        self.default_bit_rate.set_subtitle("Number of bits taken to store each sample")
        self.default_bit_rate.set_model(Gtk.StringList.new(['8 bit', '16 bit', '32 bit']));
        self.default_bit_rate.set_selected(1)
        self.audio_default_settings.add(self.default_bit_rate)

        # TODO resolution - bit rate and sample rate
    def get_audio_system_select(self, value, config_value):
        value = "automatic"
        return True

    def set_audio_system_select(self, value, config_value):
        return "automatic"

    def on_audio_system_selected(self, widget, paramspec):
        selected_value = widget.props.selected
        self.settings.set_int('audio-system', selected_value)
