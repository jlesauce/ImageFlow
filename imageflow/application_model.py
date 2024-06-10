from PyQt6.QtCore import QSettings


class ApplicationModel:
    APPLICATION_NAME = 'ImageFlow'
    APPLICATION_SHORT_NAME = 'imageflow'

    def __init__(self):
        self.application_name = ApplicationModel.APPLICATION_NAME
        self.settings = QSettings(ApplicationModel.APPLICATION_SHORT_NAME)
        self._init_settings()

    def _init_settings(self):
        self.settings.setValue('ui/select_path_dialog_title', 'Select Path')

    def get_setting(self, key):
        if not self.settings.contains(key):
            raise Exception(f"Setting key '{key}' not found")
        return self.settings.value(key)
