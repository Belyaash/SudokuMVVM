from Model.SudokuRealization.SudokuAppModel.sudokuAppModel import SudokuAppModel
from Model.Time import Time, time_class
from ViewModel.MainViewModel import view_model


class Model:
    time: Time
    sudoku_model: SudokuAppModel

    def __init__(self, len_of_side):
        self.sudoku_model = SudokuAppModel(len_of_side)
        self.time = time_class
        self.update_possible_time()

        self.sudoku_model.on_change("game_grid", lambda x: self.update_game_grid())
        self.time.on_change(self.time.CURRENT_TIME, lambda x: self.update_current_time())
        view_model.on_change("difficulty", lambda x: self.update_possible_time())
        view_model.on_change("len_of_side", lambda x: self.update_possible_time())
        view_model.on_change("is_game_stopped", lambda x: self.start_stop_timer())

    def new_game(self):
        self.sudoku_model.set_length_of_block(int(view_model.len_of_side))
        self.sudoku_model.set_difficulty(view_model.difficulty)
        self.sudoku_model.new_game()

        view_model.is_grid_created = True
        view_model.is_game_stopped = False
        view_model.current_time = "00:00:00"
        view_model.best_time = self.time.get_time(str(view_model.difficulty) + view_model.len_of_side)

    def update_game_grid(self):
        view_model.grid = self.sudoku_model.game_grid
        if self.sudoku_model.is_player_win():
            view_model.is_game_stopped = True

    def update_possible_time(self):
        view_model.possible_best_time = self.time.get_time(str(view_model.difficulty) + view_model.len_of_side)

    def update_current_time(self):
        view_model.current_time = self.time.get_current_time()

    def start_stop_timer(self):
        if view_model.is_game_stopped:
            self.time.stop_timer()
            str_to_saver = str(view_model.difficulty) + view_model.len_of_side
            self.time.save_time(str_to_saver, self.time.compare_time(view_model.current_time, view_model.best_time))
        else:
            self.time.refresh_timer()
            self.time.start_timer()


main_model = Model(int(2))
