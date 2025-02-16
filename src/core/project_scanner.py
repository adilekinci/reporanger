import os
import json

from src.config.settings_reader import get_config


def find_spring_projects() -> dict:
    dev_path = get_config("base_path")
    prefix = get_config("project_prefix") or ""

    projects_map = {}
    for root, dirs, files in os.walk(dev_path):
        if "pom.xml" in files:
            folder_name = os.path.basename(root)
            if folder_name.startswith(prefix):
                normalized_root = os.path.normpath(root)
                projects_map[folder_name] = normalized_root
    return projects_map


