import logging
from pathlib import Path

from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtWidgets import QMessageBox, QApplication
from observable import Observable

from imageflow.application_controller import ApplicationController
from imageflow.application_model import ApplicationModel
from imageflow.ui.design.ui_design_file import UiDesignFile

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    EVENT_ID_ON_CLOSE_BUTTON_CLICKED = 'close_event'

    def __init__(self, model: ApplicationModel, controller: ApplicationController):
        super().__init__()
        self._model = model
        self._controller = controller
        self._event_listeners = Observable()
        self._selection_path = None
        self._raw_path = None
        self._output_path = None

        uic.loadUi(UiDesignFile('main_window.ui').path, self)
        self._init_ui()

    def add_event_listener(self, function, event_id: str):
        self._event_listeners.on(event_id, function)

    def closeEvent(self, event):
        logger.debug(f'Notify {self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED} received')
        self._event_listeners.trigger(self.EVENT_ID_ON_CLOSE_BUTTON_CLICKED, event)
        event.accept()

    @staticmethod
    def show_error_message(message: str, title='Oups!'):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

    @staticmethod
    def show_user_confirmation_message(yes_action, no_action, message: str, title='Are you sure?'):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Question)
        yes_button = box.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        _ = box.addButton("No", QMessageBox.ButtonRole.NoRole)
        box.exec()

        return yes_action() if box.clickedButton() == yes_button else no_action()

    @staticmethod
    def set_waiting_cursor(is_enable: bool):
        if is_enable:
            QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    def _init_ui(self):
        self.setWindowTitle(self._model.application_name)
        self._init_ui_actions()

    def _init_ui_actions(self):
        self.menu_action_exit.triggered.connect(QApplication.instance().quit)
        self.select_selection_path_button.clicked.connect(self._select_selection_path)
        self.select_raw_path_button.clicked.connect(self._select_raw_path)
        self.select_output_path_button.clicked.connect(self._select_output_path)
        self.move_selection_button.clicked.connect(self._move_selection)

    def _move_selection(self):
        if not self._selection_path:
            self.show_error_message('Please select a selection path')
            return
        if not self._raw_path:
            self.show_error_message('Please select a raw path')
            return
        if not self._output_path:
            self.show_error_message('Please select an output path')
            return

        self.show_user_confirmation_message(self._move_files, lambda: None,
                                            message='Are you sure you want to move the files?')

    def _move_files(self):
        files_to_move = [Path(self._raw_path, file_name) for file_name
                         in self._get_all_items_from_output_list()]
        self._controller.move_files(files_to_move, self._raw_path, self._output_path)

    def _get_all_items_from_output_list(self):
        items = []
        for i in range(self.output_list.count()):
            items.append(self.output_list.item(i).text())
        return items

    def _select_selection_path(self):
        folder_path = self._ask_user_to_select_path()
        if folder_path:
            self._selection_path = folder_path
            self.edit_selection_path.setText(str(folder_path))
            self._update_selection_list(folder_path)

    def _select_raw_path(self):
        folder_path = self._ask_user_to_select_path()
        if folder_path:
            self._raw_path = folder_path
            self.edit_raw_path.setText(str(folder_path))

        if self._selection_path:
            self._update_output_list()

    def _select_output_path(self):
        folder_path = self._ask_user_to_select_path()
        if folder_path:
            self._output_path = folder_path
            self.edit_output_path.setText(str(folder_path))

    def _update_selection_list(self, folder_path: Path):
        self.selection_list.clear()
        for file in folder_path.iterdir():
            self.selection_list.addItem(file.name)

        if self._raw_path:
            self._update_output_list()

    def _update_output_list(self):
        output_list = self._controller.find_common_files(self._raw_path, self._selection_path)
        self.output_list.clear()
        for file in output_list:
            self.output_list.addItem(file.name)

    def _ask_user_to_select_path(self, default_path: Path = None) -> Path | None:
        logger.debug('Open select path dialog')
        folder_path = QFileDialog.getExistingDirectory(self,
                                                       self._model.get_setting("ui/select_path_dialog_title"),
                                                       str(default_path) if default_path else None)
        if folder_path:
            logger.info(f'Selected path: {folder_path}')
            return Path(folder_path)
        else:
            logger.info('No path selected')
            return None
