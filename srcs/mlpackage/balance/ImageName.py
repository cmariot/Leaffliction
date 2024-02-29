class ImageName():

    def __init__(self, full_name: str):
        r = full_name.rfind(".")
        if (r == -1):
            self.extension = None
            self.name = full_name
        else:
            self.extension = full_name[r + 1:]
            self.name = full_name[:full_name.rfind(".")]
        self.number = 0

    def get_name(self):
        if self.extension is None:
            if (self.number == 0):
                return self.name
            return self.name + "(" + str(self.number) + ")"
        else:
            if (self.number == 0):
                return self.name + "." + self.extension
            return str(
                self.name + "(" + str(self.number) + ")" + "." + self.extension
            )

    def increment(self):
        self.number += 1
