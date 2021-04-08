class CustomQueue:
    def __init__(self, src_list=None):
        """

        :type src_list: list
        """
        if src_list:
            if isinstance(src_list, list):
                self.queue = src_list
            else:
                raise Exception('Invalid argument type: src_list')
        else:
            self.queue = []

    def get(self):
        element = self.queue[0]
        self.queue.pop(0)
        return element

    def put(self, element):
        self.queue.append(element)

    def reinsert(self, element):
        self.queue.insert(0, element)

    def peek(self):
        return self.queue[0]

    def empty(self):
        if len(self.queue):
            return False
        else:
            return True

    def clear(self):
        while len(self.queue):
            self.queue.pop()

    def __str__(self):
        return self.queue.__str__()


class CharArray:
    def __init__(self):
        self.content = []
        self.length = 0

    def append(self, element):
        self.content.append(element)
        self.length += 1

    def insert(self, index, element):
        self.content.insert(index, element)
        self.length += 1

    def pop(self, index=None):
        try:
            if index:
                self.content.pop(index)
                self.length -= 1
            else:
                self.content.pop(self.length)
                self.length -= 1
        except IndexError:
            raise IndexError
        except Exception:
            raise Exception("Empty array.")

    def clear(self):
        self.content.clear()
        self.length = 0

    def to_string(self):
        return "".join(self.content)

    def __str__(self):
        return self.content.__str__()


class ColoredText:
    WARNING = '\033[91m'
    NORMAL = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
