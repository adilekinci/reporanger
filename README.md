# RepoRanger

## Project Purpose

This is a project which will be implemented with GitHub Copilot. The aim of this project is to examine how GitHub Copilot works and how performant it is.

## Project Overview

RepoRanger is designed to manage and update multiple projects efficiently. It provides a user-friendly interface to monitor and control the update process of various projects. The application integrates with external tools like Maven and Git to ensure smooth project operations and dependency management.

### How the Application Works

Application scans the whole Maven application under the folder which is defined in `settings.toml`. If you define a prefix, it will scan and list only the projects with the given prefix. The path for projects needs to be defined in the `settings.toml` file.

1. **Project Scanning**: The `project_scanner.py` module in the `core` directory scans the projects to identify their current state and dependencies.
2. **Git Integration**: The `git_client.py` and `git_flows.py` modules in the `integration/git` directory handle Git operations such as cloning repositories, checking out branches, and merging changes.
3. **Maven Integration**: The `maven_client.py`, `maven_conflict_checker.py`, and `maven_flow.py` modules in the `integration/maven` directory manage Maven operations, including building projects and checking for dependency conflicts.
4. **Process Management**: The `process.py` and `project_operations.py` modules in the `processor` directory manage the execution of various tasks and operations on the projects.
5. **User Interface**: The `ui` directory contains modules for different screens and components of the user interface, built with the Textual library. This includes the main application screen (`main_app.py`), help screen (`help_screen.py`), log screen (`log_screen.py`), overview screen (`overview_screen.py`), settings screen (`settings_screen.py`), and update screen (`update_secreen.py`).
6. **Logging**: The `logger_setup.py` module in the `utils` directory sets up logging for the application to track its operations and errors.

## Features

- **Update Projects**: Start and monitor the update process for multiple projects.
- **Stop Updates**: Stop the update process at any time.
- **User Interface**: A clean and simple UI built with the Textual library.

## Requirements

- Python 3.10+
- Textual
- Psutil

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/RepoRanger.git
    cd RepoRanger
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements
    ```

## Usage

Run the application using the following command:
```sh
python reporanger.py
```

## Project Structure

- `config/`: Configuration files for commands and settings.
- `logs/`: Log files.
- `src/`: Source code of the application.
  - `ui/`: User interface components.
  - `core/`: Core functionalities.
  - `integration/`: Integration with external tools.
  - `utils/`: Utility functions and helpers.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
