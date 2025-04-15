class Node:
    """Base node class for linear data structures."""

    def __init__(self, data=None):
        self.data = data
        self.next = None
        # Generate a simple memory address simulation
        self.memory_address = id(self)

    def __str__(self):
        return str(self.data)


class DoubleNode(Node):
    """Node for doubly linked lists."""

    def __init__(self, data=None):
        super().__init__(data)
        self.prev = None


class TreeNode(Node):
    """Node for binary trees."""

    def __init__(self, data=None):
        super().__init__(data)
        self.left = None
        self.right = None
        self.next = None  # This can be used for level order traversal