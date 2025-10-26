# FC26 SBC Solver GUI Runner
Write-Host "Starting FC26 SBC Solver GUI..."
Write-Host "Activating virtual environment..."

# Activate the virtual environment
.\fc26_env\Scripts\Activate.ps1

# Run the GUI
Write-Host "Running GUI..."
python gui_interface.py