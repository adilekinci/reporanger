from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical, ScrollableContainer
import threading
import time
import os

from src.utils.logger_setup import get_log_file, global_logger as logger

class LogScreen(Screen):

    CSS_PATH = "styles/style.tcss"

    BINDINGS = [
        ("b", "back", "Back"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, project_name, **kwargs):
        super().__init__(**kwargs)
        self.project_name = project_name
        self.stop_event = threading.Event()

    def compose(self):
        yield Header()
        yield Footer()
        with Vertical():
            self.log_panel = ScrollableContainer(Static(f"Loading logs for {self.project_name} ...", id="log-panel"))
            yield self.log_panel

    def on_mount(self):
        self.log_widget = self.query_one("#log-panel", Static)
        self.read_logs()

    def read_logs(self):
        log_file_path = get_log_file(self.project_name)
        self.update_log_panel(f"Log file path: {log_file_path}")
        def read_log_file():
            with open(log_file_path, "r") as log_file:
                while not self.stop_event.is_set():
                    line = log_file.readline()
                    if not line:
                        time.sleep(0.1)
                        log_file.seek(0, os.SEEK_CUR)  # Ensure the file pointer is at the current position
                        continue
                    #logger.debug(f"Read line: {line.strip()}")
                    self.app.call_from_thread(self.update_log_panel, line.strip())
        
        self.log_thread = threading.Thread(target=read_log_file, daemon=True)
        self.log_thread.start()

    def update_log_panel(self, line):
        #logger.debug(f"Updating log panel with line: {line}")
        self.log_widget.update(self.log_widget.renderable + "\n" + line)

    def action_back(self):
        self.stop_event.set()
        self.app.pop_screen()

    def action_quit(self):
        self.stop_event.set()
        self.app.exit()