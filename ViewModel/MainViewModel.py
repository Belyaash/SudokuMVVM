import numpy

from ReactiveModel import ReactiveModel
from Saver.saver import Saver


class MainViewModel(ReactiveModel):
    len_of_side: str
    difficulty: int
    grid: numpy.array
    current_time: str
    best_time: str
    possible_best_time: str
    is_game_stopped: bool
    is_grid_created: bool

    def __init__(self):
        super().__init__()
        self.len_of_side = "2"
        self.difficulty = 0

        full_side_len = int(self.len_of_side)**2
        self.grid = numpy.zeros((full_side_len, full_side_len), int)
        self.current_time = "--:--:--"
        self.best_time = "--:--:--"
        # self.possible_best_time = main_model.time.get_time(str(self.difficulty) + self.len_of_side)
        self.is_game_stopped = True
        self.is_grid_created = False


view_model = MainViewModel()
