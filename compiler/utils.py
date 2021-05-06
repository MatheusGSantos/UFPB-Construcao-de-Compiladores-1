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


class ScopeStack:
    def __init__(self, scope_mark="$"):
        self.stack = []
        self.length = 0
        self.scope_mark = scope_mark

    def push(self, element):
        """
        Push 'element' into stack if 'element' is not already declared in the current scope

        Raise exception if 'element' is already declared in the current scope
        """
        if not self.length or not self.in_scope(element):
            self.stack.append(element)
            self.length += 1
        else:
            raise Exception(f"Token '{element}' already declared in current scope.")

    def pop(self):
        """
        Remove and return last item

        Return None if stack is empty
        """
        if self.length:
            self.length -= 1
            return self.stack.pop()
        return None

    def peek(self):
        return self.stack[-1]

    def new_scope(self):
        self.stack.append(self.scope_mark)
        self.length += 1

    def close_scope(self):
        if not self.length:
            raise Exception(f"Empty stack. Couldn't close the current scope because there's no scope")

        for i in range(self.length, 0, -1):
            if self.pop() == self.scope_mark:
                return

        raise Exception(f"Stack base is not '{self.scope_mark}'. Couldn't close the current scope")

    def in_scope(self, element):
        """
        Checks if 'element' is declared in the scope stack. Return True if it is, False otherwise

        Raise exception if stack base is not a scope mark
        """
        if self.length:
            for i in range(self.length, 0, -1):
                if self.stack[i - 1] == element:
                    return True

            if self.stack[0] == self.scope_mark:
                return False
            else:
                raise Exception(
                    f"Reached stack base. Couldn't find {element} in the current scope because there's no scope")

        raise Exception(f"Empty stack. Couldn't find {element} in the current scope because there's no scope")


class ColoredText:
    WARNING = '\033[91m'
    NORMAL = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
