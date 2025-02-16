from textual.app import App
from src.ui.overview_screen import OverviewScreen
from src.ui.settings_screen import SettingsScreen
from src.config.settings_reader import get_config
import os
from src.utils.logger_setup import global_logger as logger

class Main(App):

    def on_mount(self):
        base_path = get_config("base_path", None)
        if not base_path or base_path.strip() == "":
            self.push_screen(SettingsScreen())
        else:
            self.push_screen(OverviewScreen())
        self.delete_log_files()

    def delete_log_files(self):
        log_dir = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
        for log_file in os.listdir(log_dir):
            if log_file != "app.log":
                os.remove(os.path.join(log_dir, log_file))
                logger.info(f"{log_file} is deleted")