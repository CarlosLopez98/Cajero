class Queue:
    def __init__(self):
        self.elements = []

    def join(self, data):
        self.elements.append(data)
        return data

    def attend(self):
        element = self.elements[0]
        return element

    def pop(self):
        self.elements.pop(0)

    def rear(self):
        return self.elements[-1]

    def front(self):
        return self.elements[0]

    def count(self):
        return len(self.elements)

    def is_empty(self):
        return len(self.elements) == 0
