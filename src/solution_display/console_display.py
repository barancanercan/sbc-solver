from enum import Enum


class CsvHeaders(Enum):
    ID = "ID"
    Name = "Name"
    Position = "Position"
    OverallRating = "OverallRating"
    Version = "Version"
    Price = "Price"
    League = "League"
    Nationality = "Nationality"
    Club = "Club"
    Futwiz = "Futwiz"
    
    def __str__(self):
        return self.value


class SbcSolutionConsoleDisplay:
    def __init__(self, solution_cards, formation):
        self.solution_cards = solution_cards
        self.formation = formation

    def display(self):
        if not self.solution_cards:
            print("No solution found!")
            return

        # Calculate total price
        total_price = sum(card[str(CsvHeaders.Price)] for card in self.solution_cards)

        # Print header
        print(f"\nSBC solved in: ?s")  # Time would be passed from solver
        print(f"+{'-' * 135}+")
        print(f"|{'SBC solution cards, Total Price = ' + str(total_price):^135}|")
        print(f"+{'-' * 135}+")
        
        # Print column headers
        print(f"| {'Name':<17} | {'Position':<8} | {'Rating':<6} | {'Version':<9} | {'Price':<5} | {'League':<12} | {'Nationality':<13} | {'Futwiz':<61} |")
        print(f"+{'-' * 135}+")

        # Print card data
        for card in self.solution_cards:
            name = card[str(CsvHeaders.Name)][:17] if len(card[str(CsvHeaders.Name)]) > 17 else card[str(CsvHeaders.Name)]
            position = card[str(CsvHeaders.Position)]
            rating = card[str(CsvHeaders.OverallRating)]
            version = card[str(CsvHeaders.Version)][:9] if len(card[str(CsvHeaders.Version)]) > 9 else card[str(CsvHeaders.Version)]
            price = card[str(CsvHeaders.Price)]
            league = card[str(CsvHeaders.League)][:12] if len(card[str(CsvHeaders.League)]) > 12 else card[str(CsvHeaders.League)]
            nationality = card[str(CsvHeaders.Nationality)][:13] if len(card[str(CsvHeaders.Nationality)]) > 13 else card[str(CsvHeaders.Nationality)]
            futwiz = card[str(CsvHeaders.Futwiz)][:61] if len(card[str(CsvHeaders.Futwiz)]) > 61 else card[str(CsvHeaders.Futwiz)]
            
            print(f"| {name:<17} | {position:<8} | {rating:<6} | {version:<9} | {price:<5} | {league:<12} | {nationality:<13} | {futwiz:<61} |")

        print(f"+{'-' * 135}+")