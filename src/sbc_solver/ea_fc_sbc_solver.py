from ortools.sat.python import cp_model
from enum import Enum
import src.sbc_solver.exceptions as SolverExceptions
import time
import pandas as pd

from typing import List


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


class EaFcSbcSolver:
    _MAX_PLAYERS_IN_FORMATION = 11

    def __init__(self, ea_fc_cards_df, formation: List[str], max_time_for_solution_s=30):
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._solver.parameters.num_workers = 8
        self._solver.parameters.max_time_in_seconds = max_time_for_solution_s

        if len(formation) > self._MAX_PLAYERS_IN_FORMATION:
            raise SolverExceptions.IncorrectFormation(
                f"Too many players in formation. Max players per formation = {EaFcSbcSolver._MAX_PLAYERS_IN_FORMATION}")
        self._formation = formation
        self._no_players = len(formation)
        # Convert enum values to strings for pandas indexing
        position_header = str(CsvHeaders.Position)
        position_values = [str(pos) for pos in self._formation]
        self._ea_fc_cards_df = ea_fc_cards_df[ea_fc_cards_df[position_header].isin(position_values)]
        self._no_cards = len(self._ea_fc_cards_df)
        id_header = str(CsvHeaders.ID)
        self._cards_bools_vars = [self._model.NewBoolVar(f'{self._ea_fc_cards_df[id_header].iloc[i]}') for i in
                                  range(self._no_cards)]
        self._leagues_bools = []
        self._nationality_bools = []
        self._solved = False
        self._player_chemistry = [self._model.NewIntVar(0, 3, f"player_{i}_chemistry") for i in range(self._no_cards)]

        # Formation constraint
        self._add_constraint_to_formation()

    def set_min_cards_with_club(self, club: str, no_players):
        club_header = str(CsvHeaders.Club)
        club_arr = self._ea_fc_cards_df[club_header].unique()
        club_map_to_unique_id = self._get_map_attribute_to_number(club_arr)
        if not club_map_to_unique_id.get(club):
            raise SolverExceptions.IncorrectClubName(f"Club name: {club} is not on the list")

        self._model.add(
            sum(
                (1 if self._ea_fc_cards_df[club_header].iloc[i] == club else 0) * self._cards_bools_vars[i] for i in
                range(self._no_cards)
            ) >= no_players
        )

    def set_min_cards_with_nation(self, nation: str, no_players):
        nation_header = str(CsvHeaders.Nationality)
        nation_arr = self._ea_fc_cards_df[nation_header].unique()
        nation_map_to_unique_id = self._get_map_attribute_to_number(nation_arr)
        if nation_map_to_unique_id.get(nation) is None:
            raise SolverExceptions.IncorrectNationName(f"Nation name: {nation} is not on the list")

        self._model.add(
            sum(
                (1 if self._ea_fc_cards_df[nation_header].iloc[i] == nation else 0) * self._cards_bools_vars[i]
                for i in range(self._no_cards)
            ) >= no_players
        )

    def set_min_cards_with_league(self, league: str, no_players):
        league_header = str(CsvHeaders.League)
        league_arr = self._ea_fc_cards_df[league_header].unique()
        league_map_to_unique_id = self._get_map_attribute_to_number(league_arr)
        if league_map_to_unique_id.get(league) is None:
            raise SolverExceptions.IncorrectLeagueName(f"League name: {league} is not on the list")

        self._model.add(
            sum(
                (1 if self._ea_fc_cards_df[league_header].iloc[i] == league else 0) * self._cards_bools_vars[i] for
                i in range(self._no_cards)
            ) >= no_players
        )

    def set_min_cards_with_version(self, version: str, no_players):
        version_header = str(CsvHeaders.Version)
        version_arr = self._ea_fc_cards_df[version_header].unique()
        version_map_to_unique_id = self._get_map_attribute_to_number(version_arr)
        if version_map_to_unique_id.get(version) is None:
            raise SolverExceptions.IncorrectVersion(f"Version: {version} is not on the list")

        self._model.add(
            sum(
                (1 if self._ea_fc_cards_df[version_header].iloc[i].strip() == version else 0) *
                self._cards_bools_vars[i] for
                i in range(self._no_cards)
            ) >= no_players
        )

    def set_min_rare_cards(self, no_players):
        version_header = str(CsvHeaders.Version)
        self._model.add(
            sum(
                (1 if self._is_card_version_rare(self._ea_fc_cards_df[version_header].iloc[i].strip()) else 0) *
                self._cards_bools_vars[i] for
                i in range(self._no_cards)
            ) >= no_players
        )

    def set_min_cards_with_overall(self, no_players, overall):
        rating_header = str(CsvHeaders.OverallRating)
        self._model.add(
            sum(
                (1 if self._ea_fc_cards_df[rating_header].iloc[i] == overall else 0) *
                self._cards_bools_vars[i] for
                i in range(self._no_cards)
            ) >= no_players
        )

    def set_max_leagues_for_solution(self, max_leagues):
        league_header = str(CsvHeaders.League)
        leagues_arr = self._ea_fc_cards_df[league_header].unique()
        league_map_to_unique_id = self._get_map_attribute_to_number(leagues_arr)

        league_vars = [self._model.NewIntVar(0, len(leagues_arr) - 1, f"League_{i}") for i in range(max_leagues)]

        for i in range(self._no_cards):
            is_league = [self._model.NewBoolVar(f'Is_League_{i}') for i in range(max_leagues)]
            for j in range(max_leagues):
                self._model.add(league_vars[j] == league_map_to_unique_id[
                    self._ea_fc_cards_df[league_header].iloc[i]]).OnlyEnforceIf(is_league[j])
            self._model.AddBoolOr(is_league).OnlyEnforceIf(self._cards_bools_vars[i])

    def set_max_nations_for_solution(self, max_nations):
        nation_header = str(CsvHeaders.Nationality)
        nation_arr = self._ea_fc_cards_df[nation_header].unique()
        nation_map_to_unique_id = self._get_map_attribute_to_number(nation_arr)

        nation_vars = [self._model.NewIntVar(0, len(nation_arr) - 1, f"Nation_{i}") for i in range(max_nations)]

        for i in range(self._no_cards):
            is_nation = [self._model.NewBoolVar(f'Is_Nation_{i}') for i in range(max_nations)]
            for j in range(max_nations):
                self._model.add(nation_vars[j] == nation_map_to_unique_id[
                    self._ea_fc_cards_df[nation_header].iloc[i]]).OnlyEnforceIf(is_nation[j])
            self._model.AddBoolOr(is_nation).OnlyEnforceIf(self._cards_bools_vars[i])

    def set_min_unique_leagues(self, no_leagues):
        if not self._leagues_bools:
            self._init_unique_leagues()

        self._model.add(sum(self._leagues_bools) >= no_leagues)

    def set_max_unique_leagues(self, no_leagues):
        if not self._leagues_bools:
            self._init_unique_leagues()

        self._model.add(sum(self._leagues_bools) <= no_leagues)

    def set_min_unique_nations(self, no_nations):
        if not self._nationality_bools:
            self._init_unique_nations()

        self._model.add(sum(self._nationality_bools) >= no_nations)

    def set_exact_unique_nations(self, no_nations):
        if not self._nationality_bools:
            self._init_unique_nations()

        self._model.add(sum(self._nationality_bools) == no_nations)

    def set_max_unique_nations(self, no_nations):
        if not self._nationality_bools:
            self._init_unique_nations()

        self._model.add(sum(self._nationality_bools) <= no_nations)

    def set_min_team_chemistry(self, min_chemistry):
        self._model.add(sum(self._player_chemistry) >= min_chemistry)

    def set_min_overall_of_squad(self, min_overall):
        rating_header = str(CsvHeaders.OverallRating)
        self._model.add(
            sum(
                self._ea_fc_cards_df[rating_header].iloc[i] * self._cards_bools_vars[i] for i in
                range(self._no_cards)
            ) >= min_overall * self._no_players
        )

    def _add_constraint_to_formation(self):
        position_header = str(CsvHeaders.Position)
        # Each position in formation must be filled exactly once
        position_count = {}
        for pos in self._formation:
            position_count[str(pos)] = position_count.get(str(pos), 0) + 1

        for position, count in position_count.items():
            self._model.add(
                sum(
                    (1 if self._ea_fc_cards_df[position_header].iloc[i] == position else 0) *
                    self._cards_bools_vars[i] for i in range(self._no_cards)
                ) == count
            )

        # Total players constraint
        self._model.add(sum(self._cards_bools_vars) == self._no_players)

    def _get_map_attribute_to_number(self, attribute_arr):
        return {attr: i for i, attr in enumerate(attribute_arr)}

    def _is_card_version_rare(self, version):
        rare_versions = ["TOTW", "TOTS", "TOTY", "ICON", "HERO", "CB", "SBC", "PINK", "TEAL", "PURPLE", "BLUE", "UNKNOWN"]
        return any(rare in version.upper() for rare in rare_versions)

    def _init_unique_leagues(self):
        league_header = str(CsvHeaders.League)
        leagues_arr = self._ea_fc_cards_df[league_header].unique()
        league_map_to_unique_id = self._get_map_attribute_to_number(leagues_arr)
        self._leagues_bools = [self._model.NewBoolVar(f'league_{i}') for i in range(len(leagues_arr))]

        for i, league in enumerate(leagues_arr):
            league_cards = [
                self._cards_bools_vars[j] for j in range(self._no_cards)
                if self._ea_fc_cards_df[league_header].iloc[j] == league
            ]
            if league_cards:
                # If any card of this league is selected, league_bool should be true
                self._model.add(sum(league_cards) > 0).OnlyEnforceIf(self._leagues_bools[i])
                self._model.add(sum(league_cards) == 0).OnlyEnforceIf(self._leagues_bools[i].Not())

    def _init_unique_nations(self):
        nation_header = str(CsvHeaders.Nationality)
        nation_arr = self._ea_fc_cards_df[nation_header].unique()
        nation_map_to_unique_id = self._get_map_attribute_to_number(nation_arr)
        self._nationality_bools = [self._model.NewBoolVar(f'nation_{i}') for i in range(len(nation_arr))]

        for i, nation in enumerate(nation_arr):
            nation_cards = [
                self._cards_bools_vars[j] for j in range(self._no_cards)
                if self._ea_fc_cards_df[nation_header].iloc[j] == nation
            ]
            if nation_cards:
                # If any card of this nation is selected, nationality_bool should be true
                self._model.add(sum(nation_cards) > 0).OnlyEnforceIf(self._nationality_bools[i])
                self._model.add(sum(nation_cards) == 0).OnlyEnforceIf(self._nationality_bools[i].Not())

    def solve(self):
        # Objective: minimize total price
        price_header = str(CsvHeaders.Price)
        self._model.minimize(
            sum(
                self._ea_fc_cards_df[price_header].iloc[i] * self._cards_bools_vars[i] for i in range(self._no_cards)
            )
        )

        print(f"Solving with {self._no_cards} cards and {self._no_players} positions")
        
        start_time = time.time()
        status = self._solver.Solve(self._model)
        end_time = time.time()

        print(f"Solver status: {status}")
        print(f"Solver time: {end_time - start_time}s")

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            self._solved = True
            solution_cards = []
            for i in range(self._no_cards):
                if self._solver.Value(self._cards_bools_vars[i]):
                    solution_cards.append(self._ea_fc_cards_df.iloc[i])
            print(f"SBC solved in: {end_time - start_time}s")
            return solution_cards
        else:
            raise SolverExceptions.NoSolutionFound("No solution found for given constraints")