# FC26 SBC Solver

This is a Python application for solving SBC (Squad Building Challenges) in FIFA 26 Ultimate Team.

## Features

- Automated SBC solving using constraint programming
- Multiple formation support
- Player data from multiple sources (FUTBIN, FutDB, CSV)
- Extensible constraint system
- Graphical User Interface (GUI)

## Installation

1. Create a virtual environment:
   ```
   python -m venv fc26_env
   ```

2. Activate the virtual environment:
   ```
   # Windows
   fc26_env\Scripts\activate
   
   # macOS/Linux
   source fc26_env/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements_fc26.txt
   ```

## Usage

### Command Line Interface

Run the main application:
```
python main_fc26.py
```

### Graphical User Interface

Run the GUI application:
```
python gui_interface.py
```

Or use the provided scripts:
- Windows: `run_gui.bat` or `run_gui.ps1`

See [README_GUI.md](README_GUI.md) for detailed GUI instructions.

## Project Structure

- `main_fc26.py`: Main application entry point
- `gui_interface.py`: Graphical user interface
- `src/`: Source code directory
  - `data/`: Data providers for player information
  - `sbc_solver/`: SBC solving engine
  - `solution_display/`: Solution display utilities
  - `utils/`: Utility functions
- `players.csv`: Sample player data
- `requirements_fc26.txt`: Python dependencies

## Requirements

- Python 3.7+
- All packages listed in requirements_fc26.txt
- Google OR-Tools for constraint solving

## License

This project is licensed under the MIT License.