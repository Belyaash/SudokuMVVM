import copy

from PyQt5 import QtCore

from ReactiveModel import ReactiveModel
from Saver.saver import Saver


class Time(ReactiveModel):
    timer: QtCore.QTimer = QtCore.QTimer()
    __seconds: int
    current_time: str
    CURRENT_TIME = "timer_current_time"

    def __init__(self):
        super().__init__()
        self.timer.timeout.connect(self.__timer_tick)
        self.timer.setInterval(1000)
        self.current_time = "00:00:00"
        self.__seconds = 0

    def __timer_tick(self):
        self.__seconds += 1
        self.current_time = self.get_current_time()

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def refresh_timer(self):
        self.__seconds = 0
        self.current_time = "00:00:00"

    def get_current_time(self):
        hours = self.__seconds // 3600
        minutes = (self.__seconds - hours * 3600) // 60
        seconds = (self.__seconds - hours * 3600 - minutes * 60)

        return (self.__convert_int_to_time_presentation(hours) + ":"
                + self.__convert_int_to_time_presentation(minutes) + ":"
                + self.__convert_int_to_time_presentation(seconds))

    @staticmethod
    def __convert_int_to_time_presentation(time: int) -> str:
        if time < 10:
            return "0" + str(time)
        else:
            return str(time)

    @staticmethod
    def compare_time(current_time, best_time):
        current_time_arr = copy.deepcopy(current_time).split(':')
        best_time_arr = copy.deepcopy(best_time).split(':')
        best_time_seconds = int(best_time_arr[0]) * 3600 + int(best_time_arr[1]) * 60 + int(best_time_arr[2])
        current_time_seconds = int(current_time_arr[0]) * 3600 + int(current_time_arr[1]) * 60 + int(current_time_arr[2])
        if (current_time_seconds < best_time_seconds) or (best_time_seconds == 0):
            return current_time
        return best_time

    def save_time(self, str_to_saver, time):
        Saver().save_data(str_to_saver, time)

    def get_time(self, str_to_saver):
        res = "00:00:00"
        try:
            res = Saver().get_data(str_to_saver)
        except:
            Saver().save_data(str_to_saver,res)
        return res

time_class = Time()
