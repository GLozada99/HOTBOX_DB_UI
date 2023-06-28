class Queue:
    def __init__(self) -> None:
        self.container = []

    def append_1(self, element):
        if len(self.container) == 10:
            del self.container[0]
        self.container.append(element)

    def avg(self):
        return sum(self.container) / len(self.container)
