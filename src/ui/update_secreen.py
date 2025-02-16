# update_projects_window.py

import threading
import time
from textual.screen import Screen
from textual.widgets import Static, Header, Footer
from textual.containers import Vertical, ScrollableContainer
from src.utils.logger_setup import global_logger as logger


class UpdateProjectsScreen(Screen):

    CSS_PATH = "styles/style.tcss"

    BINDINGS = [
        ("b", "back", "Back(Stops all updates)"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, projects_map: dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.projects_map = projects_map

    def compose(self):
        yield Header()
        yield Footer()
        with Vertical():
            self.detail_panel_container = ScrollableContainer(Static("Updating projects...", id="log-panel"))
            yield self.detail_panel_container


    def on_mount(self):
        self.log_widget = self.query_one("#log-panel", Static)
        self.run_updates()

    def run_updates(self):
        self.stop_event = threading.Event()
        def update_projects():
            logger.info("----------------------- Update all starts -------------------")
            log_text = ""
            for project_name, project_path in self.projects_map.items():
                if self.stop_event.is_set():
                    log_text += "\nUpdate stopped."
                    self.log_widget.update(log_text)
                    logger.info("Update stopped.")
                    return
                log_text += f"\n{project_name} ({project_path}) updating..."
                logger.info(log_text)
                self.log_widget.update(log_text)
                time.sleep(1)  # Wait for simulation
            log_text += "\n----------------------- Update all finished -------------------"
            self.log_widget.update(log_text)
            self.app.pop_screen()

        thread = threading.Thread(target=update_projects, daemon=True)
        thread.start()

    def action_back(self):
        self.stop_event.set()
        self.app.pop_screen()

    def action_quit(self):
        self.app.exit()
