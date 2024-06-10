import argparse
import logging
import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication

from imageflow.application_controller import ApplicationController
from imageflow.application_model import ApplicationModel
from imageflow.ui.main_window import MainWindow
from imageflow.utils.logger import configure_logger

logger = logging.getLogger(__name__)


def catch_exceptions(e, value, traceback):
    old_hook(e, value, traceback)
    QtWidgets.QMessageBox.critical(None, "Critical Error", f"Exception: {e}\n\n"
                                                           f"{value}")


# Redefine exception hook to catch PyQt exceptions
old_hook = sys.excepthook
sys.excepthook = catch_exceptions


def main():
    args = _parse_arguments()
    configure_logger(log_level=logging.getLevelName(args.log_level.upper()))

    try:
        model = ApplicationModel()
        logger.info(f'Start {model.application_name}')

        application = QApplication(sys.argv[:1])
        controller = ApplicationController(model)
        view = MainWindow(model, controller)

        view.add_event_listener(close_application, MainWindow.EVENT_ID_ON_CLOSE_BUTTON_CLICKED)
        view.show()
        sys.exit(application.exec())
    except Exception as e:
        logging.exception(e)


def close_application(event):
    logger.info('Close application')


def _parse_arguments():
    parser = _create_argument_parser()
    return parser.parse_args()


def _create_argument_parser():
    parser = argparse.ArgumentParser(
        description='ImageFlow is a Python-based image processing application that helps user to filter images.')
    parser.add_argument('--log-level', dest="log_level",
                        choices=['debug', 'info', 'warn', 'error', 'fatal'], default='info',
                        help="Set the application log level")
    return parser


if __name__ == "__main__":
    main()
