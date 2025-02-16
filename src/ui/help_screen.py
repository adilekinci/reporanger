from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical, Center

class HelpScreen(Screen):

    CSS_PATH = "styles/style.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("b", "back", "Back"),
    ]

    def compose(self):
        yield Header()
        with Vertical():
            with Center():
                yield Static(
                    """
                    Help Page

                    [U] Quick Update
                    - Checks out a new branch from master
                    - Updates POM files
                    - Checks for conflicts
                    - Commits changes
                    - Pushes changes

                    [U] Full Update
                    - Performs all steps in Quick Update
                    - Runs tests

                    [A] Update All
                    - Updates all projects

                    [S] Start
                    - Starts the selected project

                    [X] Stop
                    - Stops the selected project

                    [O] Open
                    - Opens the selected project in the configured editor

                    [D] Display POM
                    - Displays the POM file of the selected project

                    [Q] Quit
                    - Exits the application
                    """,
                    id="help-text"
                )
        yield Footer()

    def action_quit(self):
        self.app.exit()

    def action_back(self):
        self.app.pop_screen()
