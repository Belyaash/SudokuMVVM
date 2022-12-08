import shelve


class Saver:
    def __init__(self):
        self.file = shelve.open("results")

    def save_data(self, name: str, value):
        self.file[name] = value

    def get_data(self, name: str):
        return self.file[name]

    def __del__(self):
        self.file.close()
