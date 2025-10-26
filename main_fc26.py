from src.data.fc26_data_provider import FC26DataProvider
from src.sbc_solver.ea_fc_sbc_solver import EaFcSbcSolver
from src.utils.formations import Formations
from src.solution_display.console_display import SbcSolutionConsoleDisplay


def main():
    # Initialize the data provider
    print("Initializing FC26 Data Provider...")
    provider = FC26DataProvider()
    
    # Get players data (automatically selects best source)
    print("Fetching player data...")
    dataset = provider.get_players_data(source="auto")
    
    # Define formation
    formation = Formations.F4_1_3_2.value  # Using 4-1-3-2 formation that matches our dataset
    
    # Create solver instance
    print("Creating SBC solver...")
    sbc_solver = EaFcSbcSolver(dataset, formation)
    
    # Set some example constraints for FC26
    print("Setting SBC constraints...")
    sbc_solver.set_min_overall_of_squad(65)  # Minimum squad overall rating
    sbc_solver.set_min_cards_with_overall(3, 64)  # At least 3 players with 64 rating
    sbc_solver.set_min_unique_nations(4)  # Minimum 4 unique nations
    sbc_solver.set_min_cards_with_nation("Spain", 1)  # At least 1 Spanish player
    
    try:
        # Solve the SBC
        print("Solving SBC...")
        sbc_cards = sbc_solver.solve()
        
        # Display solution
        print("Displaying solution...")
        solution_display = SbcSolutionConsoleDisplay(sbc_cards, formation)
        solution_display.display()
        
    except Exception as e:
        print(f"Error solving SBC: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()