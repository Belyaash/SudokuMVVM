class Cell:
    num = 0
    isActive = False

    def __init__(self, num: int):
        if 0 < num < 10:
            self.num = num
            self.isActive = False
        else:
            self.num = 0
            self.isActive = True
