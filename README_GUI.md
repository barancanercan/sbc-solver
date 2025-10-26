# FC26 SBC Solver GUI

This is a simple graphical interface for the FC26 SBC Solver.

## Features

- Minimalist and lightweight interface
- Easy-to-use constraint settings
- Formation selection
- Solution export to CSV
- Real-time progress feedback

## How to Use

1. Run the GUI application:
   ```
   python gui_interface.py
   ```

2. Wait for the player data to load (shown in the output area)

3. Set your desired constraints:
   - Select a formation from the dropdown
   - Set minimum squad overall rating
   - Set minimum cards with specific rating
   - Set minimum unique nations
   - Toggle Spanish player requirement

4. Click "Solve SBC" to find a solution

5. View the solution in the output area

6. Export the solution to CSV using the "Export Solution" button

## Requirements

The GUI requires the same dependencies as the main application:
- Python 3.7+
- All packages listed in requirements_fc26.txt

Make sure to activate your virtual environment before running:
```
# Windows
fc26_env\Scripts\activate
python gui_interface.py
```