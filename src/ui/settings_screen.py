from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Static
from textual.containers import Vertical, ScrollableContainer
from src.config.settings_reader import CONFIG_PATH, reload_config
import toml

from src.ui.overview_screen import OverviewScreen

class SettingsScreen(Screen):

    CSS_PATH = "styles/style.tcss"

    BINDINGS = [
        ("s", "save", "Save"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_path = ""
        self.log_level = "DEBUG"
        self.max_projects = 50
        self.project_prefix = "web-toll"
        self.spring_profile = "local"

    def compose(self):
        yield Header()

        with ScrollableContainer():
            with Vertical():
                yield Static("Settings Configuration", id="settings-header")
                self.base_path_input = Input(placeholder="Base Path (mandatory)", id="base-path")
                yield self.base_path_input
                self.log_level_input = Input(value=self.log_level, placeholder="Log Level", id="log-level")
                yield self.log_level_input
                self.max_projects_input = Input(value=str(self.max_projects), placeholder="Max Projects", id="max-projects")
                yield self.max_projects_input
                self.project_prefix_input = Input(value=self.project_prefix, placeholder="Project Prefix", id="project-prefix")
                yield self.project_prefix_input
                self.spring_profile_input = Input(value=self.spring_profile, placeholder="Spring Profile", id="spring-profile")
                yield self.spring_profile_input

        yield Footer()

    def on_mount(self):
        self.app.refresh()

    def action_save(self):
        if not self.base_path_input.value.strip():
            return
        settings = {
            "base_path": self.base_path_input.value.strip(),
            "log_level": self.log_level_input.value.strip(),
            "max_projects": int(self.max_projects_input.value.strip()),
            "project_prefix": self.project_prefix_input.value.strip(),
            "spring_profile": self.spring_profile_input.value.strip(),
        }
        with open(CONFIG_PATH, "w") as f:
            f.write(toml.dumps(settings))

        reload_config()
        self.app.pop_screen()
        self.app.push_screen(OverviewScreen())

    def action_quit(self):
        self.app.exit()
