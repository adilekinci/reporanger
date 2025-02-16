from textual.widgets import ListItem, Static


class ProjectListItem(ListItem):
    def __init__(self, folder_name: str):
        super().__init__(Static(folder_name))
        self.folder_name = folder_name