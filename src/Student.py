class Student:

    def __init__(self, s_number, house="GUEST", do_group=""):
        self.s_number = s_number
        self.house = house
        self.do_group = do_group

    def __str__(self):
        return "{}".format(self.s_number)
