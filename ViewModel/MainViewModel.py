import numpy

from Model.model import Model
from ReactiveModel import ReactiveModel
from Saver.saver import Saver


class MainViewModel(ReactiveModel):
    model: Model
    len_of_side: str
    difficulty: str
    grid: numpy.array
    current_time: str
    best_time: str
    possible_best_time: str
    is_game_stopped: bool
    is_grid_created: bool

    def __init__(self):
        super().__init__()
        self.len_of_side = "2"
        self.difficulty = "Easy"

        self.model = Model(int(self.len_of_side))

        full_side_len = int(self.len_of_side)**2
        self.grid = numpy.zeros((full_side_len, full_side_len), int)
        self.current_time = "--:--:--"
        self.best_time = "--:--:--"
        self.possible_best_time = self.get_possible_time()
        self.is_game_stopped = True
        self.is_grid_created = False

        self.model.sudoku_model.on_change("game_grid", lambda x: self.update_game_grid())
        self.model.time.on_change(self.model.time.CURRENT_TIME, lambda x: self.update_current_time())
        self.on_change("difficulty", lambda x: self.update_possible_time())
        self.on_change("len_of_side", lambda x: self.update_possible_time())
        self.on_change("is_game_stopped", lambda x: self.start_stop_timer())
        # self.new_game()

    def get_possible_time(self):
        str_to_saver = self.difficulty + self.len_of_side
        return self.model.time.get_time(str_to_saver)

    def new_game(self):
        self.is_grid_created = True
        self.model.sudoku_model.set_length_of_block(int(self.len_of_side))
        self.model.sudoku_model.set_difficulty(self.get_num_of_difficulty())
        self.model.sudoku_model.new_game()
        self.is_game_stopped = False
        self.current_time = "00:00:00"
        self.best_time = self.get_possible_time()

    def solve(self):
        if not self.is_game_stopped:
            self.model.sudoku_model.solve()

    def set_num_in_grid(self, row, col, num):
        self.model.sudoku_model.set_cell_num(row, col, num)

    def get_num_of_difficulty(self):
        if self.difficulty == "Medium":
            return 1
        elif self.difficulty == "Hard":
            return 2
        return 0

    def update_game_grid(self):
        self.grid = self.model.sudoku_model.game_grid
        if self.model.sudoku_model.is_player_win():
            self.is_game_stopped = True

    def update_possible_time(self):
        self.possible_best_time = self.get_possible_time()

    def update_current_time(self):
        self.current_time = self.model.time.get_current_time()

    def start_stop_timer(self):
        if self.is_game_stopped:
            self.model.time.stop_timer()
            str_to_saver = self.difficulty + self.len_of_side
            self.model.time.save_time(str_to_saver, self.model.time.compare_time(self.current_time, self.best_time))
        else:
            self.model.time.refresh_timer()
            self.model.time.start_timer()


view_model = MainViewModel()
