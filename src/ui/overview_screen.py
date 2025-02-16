import os
import threading
import signal
import time
from textual.screen import Screen
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Header, Footer, ListView, Static

from src.utils.logger_setup import global_logger as logger
from src.utils.logger_setup import log_with_project as project_logger

from src.utils.logger_setup import get_log_file
from src.core.project_scanner import find_spring_projects
from src.integration.maven.maven_client import mvn_springboot_start
from src.processor.process import quick_update_flow
from src.ui.item.project_list_item import ProjectListItem
from src.ui.update_secreen import UpdateProjectsScreen
from src.ui.help_screen import HelpScreen
from src.processor.project_operations import open_project_in_vscode, kill_process
from src.ui.log_screen import LogScreen

class OverviewScreen(Screen):

    CSS_PATH = "styles/style.tcss"

    BINDINGS = [
        ("u", "quick_update", "Quick Update"),
        ("U", "full_update", "Full Update"),
        ("A", "update_all", "Update All"),
        ("s", "start", "Start"),
        ("x", "stop", "Stop"),
        ("d", "display_pom", "Display POM"),
        ("o", "open", "Open"),
        ("q", "quit", "Quit"),
        ("h", "help", "Help"),
        ("l", "show_logs", "Show Logs"),  # Add this line
    ]

    def compose(self):
        yield Header()
        yield Footer()

        with Horizontal():
            self.project_list = ListView(id="left-panel")
            yield self.project_list

            self.detail_panel_container = ScrollableContainer(Static("No project selected yet.", id="right-panel"))
            yield self.detail_panel_container

    def on_mount(self):
        self.projects_map = self.load_projects_into_list_view(self.project_list)
        self.project_list.focus()
        self.running_projects = {}
        self.log_monitor_thread = None
        self.log_monitor_running = False
        self.last_positions = {}  # Dictionary to store last read positions for each project

    def load_projects_into_list_view(self, list_view_widget):
        projects_map = find_spring_projects()
        for folder_name in projects_map:
            item = ProjectListItem(folder_name)
            list_view_widget.append(item)
        return projects_map

    def on_list_view_selected(self, event: ListView.Selected):
        proj_name = event.item.folder_name
        self.selected_project_name = proj_name
        self._update_detail_panel(f"Selected project: {proj_name}")

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        proj_name = event.item.folder_name
        self.selected_project_name = proj_name
        self._update_detail_panel(f"Selected project: {proj_name}")
    

    # ------------------ Action methods ------------------
    def action_quick_update(self):
        self._update_detail_panel(
            "Quick Update command triggered!\n"
        )
        project_path = self._get_selected_project_path()
        if not project_path:
            self._update_detail_panel("No project selected.")
            return

        thread = threading.Thread(
            target=quick_update_flow,
            args=(project_path,),
            daemon=True
        )
        thread.start()
    
    def action_full_update(self):
        self._update_detail_panel(
            "FULL Update command triggered!\n This method not implemeted yet."
        )
        
    def action_start(self):
        self._update_detail_panel("Start command triggered!\n")

        project_path = self._get_selected_project_path()
        if not project_path:
            return

        thread = threading.Thread(
            target=mvn_springboot_start,
            args=(self, project_path),
            daemon=True
        )
        thread.start()

        self._update_detail_panel("Spring Boot is starting... Logs will appear below.\n")
    
    def action_update_all(self):
        self.app.push_screen(UpdateProjectsScreen(self.projects_map))

    def action_display_pom(self):
        project_path = self._get_selected_project_path()
        if not project_path:
            return

        pom_path = os.path.join(project_path, "pom.xml")
        if not os.path.exists(pom_path):
            self._update_detail_panel("POM file not found.")
            return

        with open(pom_path, "r") as pom_file:
            pom_content = pom_file.read()

        self._update_detail_panel(pom_content)

    def action_stop(self):
        if self.selected_project_name in self.running_projects:
            pid = self.running_projects[self.selected_project_name]
            process_killed = kill_process(pid, self.selected_project_name)
            if process_killed:
                del self.running_projects[self.selected_project_name]
        else:
            logger.warning(f"No running project found with name {self.selected_project_name}")
            
    def action_open(self):
        project_path = self._get_selected_project_path()
        open_project_in_vscode(project_path)
        
    def action_quit(self):
        self.log_monitor_running = False
        self.app.exit()

    def action_help(self):
        self.app.push_screen(HelpScreen())
    
    def action_show_logs(self):
        if not hasattr(self, "selected_project_name") or not self.selected_project_name:
            self._update_detail_panel("No Project selected")
            return
        self.app.push_screen(LogScreen(self.selected_project_name))
    
    # ------------------ Helper methods ------------------


    def _update_detail_panel(self, text: str):
        detail_text_widget = self.detail_panel_container.query_one(Static)
        detail_text_widget.update(text)

    def _get_selected_project_path(self):
        if not hasattr(self, "selected_project_name") or not self.selected_project_name:
            self._update_detail_panel("No Project selected")
            return None

        project_path = self.projects_map.get(self.selected_project_name)
        if not project_path:
            self._update_detail_panel("Could not find the project path. projects_map might be incorrect.")
            return None

        return project_path