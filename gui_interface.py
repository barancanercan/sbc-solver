import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from src.data.fc26_data_provider import FC26DataProvider
from src.sbc_solver.ea_fc_sbc_solver import EaFcSbcSolver
from src.utils.formations import Formations
from src.solution_display.console_display import SbcSolutionConsoleDisplay
import pandas as pd


class FC26BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FC26 SBC Solver")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.dataset = None
        self.solution = None
        
        # Create UI
        self.create_widgets()
        
        # Load data in background
        self.load_data()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="FC26 SBC Solver", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Formation selection
        ttk.Label(main_frame, text="Formation:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.formation_var = tk.StringVar(value="4-1-3-2")
        formations = ["4-4-2", "4-1-3-2", "4-1-2-1-2", "4-2-3-1", "4-3-3", "3-5-2", "5-3-2", "5-4-1", "4-2-2-2", "4-1-4-1", "3-4-3"]
        self.formation_combo = ttk.Combobox(main_frame, textvariable=self.formation_var, values=formations, width=15, state="readonly")
        self.formation_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Constraints frame
        constraints_frame = ttk.LabelFrame(main_frame, text="Constraints", padding="10")
        constraints_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, pady=10)
        constraints_frame.columnconfigure(1, weight=1)
        
        # Minimum overall rating
        ttk.Label(constraints_frame, text="Min Squad Overall:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.min_overall_var = tk.StringVar(value="65")
        ttk.Entry(constraints_frame, textvariable=self.min_overall_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Minimum cards with overall
        ttk.Label(constraints_frame, text="Min Cards with Rating:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.min_cards_rating_frame = ttk.Frame(constraints_frame)
        self.min_cards_rating_frame.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        self.min_cards_count_var = tk.StringVar(value="3")
        ttk.Entry(self.min_cards_rating_frame, textvariable=self.min_cards_count_var, width=5).pack(side=tk.LEFT)
        
        ttk.Label(self.min_cards_rating_frame, text="with rating").pack(side=tk.LEFT, padx=(5, 5))
        
        self.min_cards_rating_var = tk.StringVar(value="64")
        ttk.Entry(self.min_cards_rating_frame, textvariable=self.min_cards_rating_var, width=5).pack(side=tk.LEFT)
        
        # Minimum unique nations
        ttk.Label(constraints_frame, text="Min Unique Nations:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.min_nations_var = tk.StringVar(value="4")
        ttk.Entry(constraints_frame, textvariable=self.min_nations_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Spanish player requirement
        self.spain_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(constraints_frame, text="At least 1 Spanish player", variable=self.spain_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.solve_button = ttk.Button(buttons_frame, text="Solve SBC", command=self.solve_sbc)
        self.solve_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(buttons_frame, text="Export Solution", command=self.export_solution, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(main_frame, height=20)
        self.output_text.grid(row=5, column=0, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S)
        self.output_text.insert(tk.END, "Welcome to FC26 SBC Solver!\nData is loading in the background...\n")
    
    def load_data(self):
        """Load player data in a separate thread"""
        def load():
            try:
                self.progress.start()
                provider = FC26DataProvider()
                self.dataset = provider.get_players_data(source="auto")
                self.root.after(0, self.on_data_loaded)
            except Exception as e:
                self.root.after(0, self.on_data_error, str(e))
        
        threading.Thread(target=load, daemon=True).start()
    
    def on_data_loaded(self):
        """Called when data loading is complete"""
        self.progress.stop()
        self.output_text.insert(tk.END, f"Data loaded successfully! {len(self.dataset) if self.dataset is not None else 0} players available.\n")
        self.output_text.see(tk.END)
        self.solve_button.config(state=tk.NORMAL)
    
    def on_data_error(self, error_msg):
        """Called when data loading fails"""
        self.progress.stop()
        self.output_text.insert(tk.END, f"Error loading data: {error_msg}\n")
        self.output_text.see(tk.END)
    
    def get_selected_formation(self):
        """Convert selected formation to the appropriate format"""
        formation_map = {
            "4-4-2": Formations.F4_4_2.value,
            "4-1-3-2": Formations.F4_1_3_2.value,
            "4-1-2-1-2": Formations.F4_1_2_1_2.value,
            "4-2-3-1": Formations.F4_2_3_1.value,
            "4-3-3": Formations.F4_3_3.value,
            "3-5-2": Formations.F3_5_2.value,
            "5-3-2": Formations.F5_3_2.value,
            "5-4-1": Formations.F5_4_1.value,
            "4-2-2-2": Formations.F4_2_2_2.value,
            "4-1-4-1": Formations.F4_1_4_1.value,
            "3-4-3": Formations.F3_4_3.value
        }
        return formation_map.get(self.formation_var.get(), Formations.F4_1_3_2.value)
    
    def solve_sbc(self):
        """Solve the SBC with current settings"""
        if self.dataset is None:
            messagebox.showerror("Error", "Data not loaded yet. Please wait.")
            return
        
        def solve():
            try:
                self.root.after(0, self.on_solve_start)
                
                # Get formation
                formation = self.get_selected_formation()
                
                # Create solver
                sbc_solver = EaFcSbcSolver(self.dataset, formation)
                
                # Apply constraints
                min_overall = int(self.min_overall_var.get())
                sbc_solver.set_min_overall_of_squad(min_overall)
                
                min_cards_count = int(self.min_cards_count_var.get())
                min_cards_rating = int(self.min_cards_rating_var.get())
                sbc_solver.set_min_cards_with_overall(min_cards_count, min_cards_rating)
                
                min_nations = int(self.min_nations_var.get())
                sbc_solver.set_min_unique_nations(min_nations)
                
                if self.spain_var.get():
                    sbc_solver.set_min_cards_with_nation("Spain", 1)
                
                # Solve
                self.solution = sbc_solver.solve()
                
                # Display solution
                solution_display = SbcSolutionConsoleDisplay(self.solution, formation)
                
                # Capture output
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                solution_display.display()
                
                sys.stdout = old_stdout
                output = captured_output.getvalue()
                
                self.root.after(0, self.on_solve_complete, output)
            except Exception as e:
                self.root.after(0, self.on_solve_error, str(e))
        
        threading.Thread(target=solve, daemon=True).start()
    
    def on_solve_start(self):
        """Called when solving starts"""
        self.solve_button.config(state=tk.DISABLED)
        self.progress.start()
        self.output_text.insert(tk.END, "Solving SBC...\n")
        self.output_text.see(tk.END)
    
    def on_solve_complete(self, output):
        """Called when solving is complete"""
        self.progress.stop()
        self.solve_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)
        
        self.output_text.insert(tk.END, "\n" + output)
        self.output_text.see(tk.END)
    
    def on_solve_error(self, error_msg):
        """Called when solving fails"""
        self.progress.stop()
        self.solve_button.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"Error solving SBC: {error_msg}\n")
        self.output_text.see(tk.END)
    
    def export_solution(self):
        """Export the current solution to a file"""
        if self.solution is None:
            messagebox.showwarning("Warning", "No solution to export.")
            return
        
        try:
            # Create a DataFrame from the solution
            # Convert solution cards to dictionaries
            solution_dicts = []
            if self.solution is not None and hasattr(self.solution, '__iter__'):
                for card in self.solution:
                    if hasattr(card, 'to_dict'):
                        solution_dicts.append(card.to_dict())
                    else:
                        solution_dicts.append(dict(card))
            df = pd.DataFrame(solution_dicts)
            
            # Save to CSV
            filename = "sbc_solution.csv"
            df.to_csv(filename, index=False)
            
            self.output_text.insert(tk.END, f"\nSolution exported to {filename}\n")
            self.output_text.see(tk.END)
            messagebox.showinfo("Success", f"Solution exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export solution: {str(e)}")


def main():
    root = tk.Tk()
    app = FC26BotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()