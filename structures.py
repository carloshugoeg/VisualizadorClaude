from nodes import *

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0
        self.max_size = float('inf')  # Can be changed if needed

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        return True

    def pop(self):
        if self.is_empty():
            return None
        popped = self.top
        self.top = self.top.next
        self.size -= 1
        return popped.data

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        return self.top is None

    def search(self, value):
        current = self.top
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1  # Not found

    def get_nodes(self):
        """Return a list of all nodes for visualization."""
        nodes = []
        current = self.top
        while current:
            nodes.append(current)
            current = current.next
        return nodes


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
        self.max_size = float('inf')

    def enqueue(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.front = new_node
        else:
            self.rear.next = new_node
        self.rear = new_node
        self.size += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data

    def peek(self):
        if self.is_empty():
            return None
        return self.front.data

    def is_empty(self):
        return self.front is None

    def search(self, value):
        current = self.front
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1  # Not found

    def get_nodes(self):
        """Return a list of all nodes for visualization."""
        nodes = []
        current = self.front
        while current:
            nodes.append(current)
            current = current.next
        return nodes


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return True

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.size += 1
            return True

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self.size += 1
        return True

    def delete_from_beginning(self):
        if not self.head:
            return None
        temp = self.head
        self.head = self.head.next
        self.size -= 1
        return temp.data

    def delete_from_end(self):
        if not self.head:
            return None

        if not self.head.next:
            temp = self.head
            self.head = None
            self.size -= 1
            return temp.data

        current = self.head
        previous = None
        while current.next:
            previous = current
            current = current.next

        previous.next = None
        self.size -= 1
        return current.data

    def search(self, value):
        current = self.head
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1  # Not found

    def get_nodes(self):
        """Return a list of all nodes for visualization."""
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        return nodes


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if not self.head:
            new_node.next = new_node  # Points to itself
            self.head = new_node
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            new_node.next = self.head
            current.next = new_node
            self.head = new_node
        self.size += 1
        return True

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            new_node.next = new_node  # Points to itself
            self.head = new_node
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head
        self.size += 1
        return True

    def delete_from_beginning(self):
        if not self.head:
            return None

        if self.head.next == self.head:  # Only one node
            temp = self.head
            self.head = None
            self.size -= 1
            return temp.data

        current = self.head
        while current.next != self.head:
            current = current.next

        temp = self.head
        self.head = self.head.next
        current.next = self.head
        self.size -= 1
        return temp.data

    def delete_from_end(self):
        if not self.head:
            return None

        if self.head.next == self.head:  # Only one node
            temp = self.head
            self.head = None
            self.size -= 1
            return temp.data

        current = self.head
        previous = None
        while current.next != self.head:
            previous = current
            current = current.next

        previous.next = self.head
        self.size -= 1
        return current.data

    def search(self, value):
        if not self.head:
            return -1

        current = self.head
        position = 0

        while True:
            if current.data == value:
                return position
            current = current.next
            position += 1
            if current == self.head:
                break

        return -1  # Not found

    def rotate_left(self):
        if not self.head or self.head.next == self.head:
            return  # Empty or only one node
        self.head = self.head.next

    def rotate_right(self):
        if not self.head or self.head.next == self.head:
            return  # Empty or only one node

        current = self.head
        while current.next != self.head:
            current = current.next

        self.head = current

    def get_nodes(self):
        """Return a list of all nodes for visualization."""
        if not self.head:
            return []

        nodes = []
        current = self.head

        while True:
            nodes.append(current)
            current = current.next
            if current == self.head:
                break

        return nodes


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = DoubleNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        return True

    def insert_at_end(self, data):
        new_node = DoubleNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
        return True

    def insert_at_position(self, position, data):
        if position < 0 or position > self.size:
            return False

        if position == 0:
            return self.insert_at_beginning(data)

        if position == self.size:
            return self.insert_at_end(data)

        new_node = DoubleNode(data)
        current = self.head
        for _ in range(position):
            current = current.next

        new_node.next = current
        new_node.prev = current.prev
        current.prev.next = new_node
        current.prev = new_node
        self.size += 1
        return True

    def delete_from_beginning(self):
        if not self.head:
            return None

        temp = self.head
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1
        return temp.data

    def delete_from_end(self):
        if not self.head:
            return None

        temp = self.tail
        if self.head == self.tail:  # Only one node
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.size -= 1
        return temp.data

    def delete_at_position(self, position):
        if position < 0 or position >= self.size:
            return None

        if position == 0:
            return self.delete_from_beginning()

        if position == self.size - 1:
            return self.delete_from_end()

        current = self.head
        for _ in range(position):
            current = current.next

        current.prev.next = current.next
        current.next.prev = current.prev
        self.size -= 1
        return current.data

    def search(self, value):
        current = self.head
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1  # Not found

    def get_nodes(self):
        """Return a list of all nodes for visualization."""
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
        return nodes


class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.height = 0

    def insert(self, parent_value, data, is_left=True):
        """
        Insert a node as a left or right child of the parent node with parent_value.
        If the tree is empty, insert as the root.
        """
        if not self.root:
            self.root = TreeNode(data)
            self.size += 1
            self.height = 1
            return True

        # Find the parent node
        parent = self._find_node(self.root, parent_value)
        if not parent:
            return False

        # Create and insert the new node
        new_node = TreeNode(data)
        if is_left:
            if parent.left:
                return False  # Left child already exists
            parent.left = new_node
        else:
            if parent.right:
                return False  # Right child already exists
            parent.right = new_node

        self.size += 1
        self._update_height()
        return True

    def _find_node(self, node, value):
        """Helper method to find a node with the given value."""
        if not node:
            return None
        if node.data == value:
            return node

        left_result = self._find_node(node.left, value)
        if left_result:
            return left_result

        return self._find_node(node.right, value)

    def delete(self, value):
        """Delete a node with the given value."""
        if not self.root:
            return False

        # Special case: deleting the root
        if self.root.data == value:
            if not self.root.left and not self.root.right:
                self.root = None
            elif not self.root.right:
                self.root = self.root.left
            elif not self.root.left:
                self.root = self.root.right
            else:
                # Root has two children, this is more complex
                # For simplicity, we're not handling this case in this example
                return False

            self.size -= 1
            self._update_height()
            return True

        # Find the parent of the node to delete
        parent = self._find_parent(self.root, value)
        if not parent:
            return False

        # Determine which child to delete
        if parent.left and parent.left.data == value:
            node_to_delete = parent.left
            if not node_to_delete.left and not node_to_delete.right:
                parent.left = None
            elif not node_to_delete.right:
                parent.left = node_to_delete.left
            elif not node_to_delete.left:
                parent.left = node_to_delete.right
            else:
                # Node has two children, this is more complex
                # For simplicity, we're not handling this case in this example
                return False
        elif parent.right and parent.right.data == value:
            node_to_delete = parent.right
            if not node_to_delete.left and not node_to_delete.right:
                parent.right = None
            elif not node_to_delete.right:
                parent.right = node_to_delete.left
            elif not node_to_delete.left:
                parent.right = node_to_delete.right
            else:
                # Node has two children, this is more complex
                # For simplicity, we're not handling this case in this example
                return False
        else:
            return False

        self.size -= 1
        self._update_height()
        return True

    def _find_parent(self, node, value):
        """Helper method to find the parent of a node with the given value."""
        if not node:
            return None

        if (node.left and node.left.data == value) or (node.right and node.right.data == value):
            return node

        left_result = self._find_parent(node.left, value)
        if left_result:
            return left_result

        return self._find_parent(node.right, value)

    def search(self, value):
        """Search for a node with the given value."""
        return bool(self._find_node(self.root, value))

    def _update_height(self):
        """Update the height of the tree."""
        if not self.root:
            self.height = 0
            return

        self.height = self._height(self.root)

    def _height(self, node):
        """Calculate the height of a subtree."""
        if not node:
            return 0

        left_height = self._height(node.left)
        right_height = self._height(node.right)

        return max(left_height, right_height) + 1

    def get_nodes_by_level(self):
        """Return a dictionary of nodes by level for visualization."""
        if not self.root:
            return {}

        result = {}
        self._get_nodes_by_level(self.root, 0, result)
        return result

    def _get_nodes_by_level(self, node, level, result):
        """Helper method to collect nodes by level."""
        if not node:
            return

        if level not in result:
            result[level] = []

        result[level].append(node)

        self._get_nodes_by_level(node.left, level + 1, result)
        self._get_nodes_by_level(node.right, level + 1, result)


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.height = 0

    def insert(self, data):
        """Insert a node with the given value."""
        if not self.root:
            self.root = TreeNode(data)
            self.size += 1
            self.height = 1
            return True

        self._insert_recursive(self.root, data)
        self._update_height()
        return True

    def _insert_recursive(self, node, data):
        """Helper method to recursively insert a value."""
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
                self.size += 1
            else:
                self._insert_recursive(node.left, data)
        else:  # data >= node.data
            if node.right is None:
                node.right = TreeNode(data)
                self.size += 1
            else:
                self._insert_recursive(node.right, data)

    def delete(self, data):
        """Delete a node with the given value."""
        if not self.root:
            return False

        result = self._delete_recursive(self.root, None, data)
        if result:
            self._update_height()
        return result

    def _delete_recursive(self, node, parent, data):
        """Helper method to recursively delete a value."""
        if not node:
            return False

        if data < node.data:
            return self._delete_recursive(node.left, node, data)
        elif data > node.data:
            return self._delete_recursive(node.right, node, data)
        else:  # Found the node to delete
            # Case 1: Node has no children
            if not node.left and not node.right:
                if parent:
                    if parent.left == node:
                        parent.left = None
                    else:
                        parent.right = None
                else:  # Deleting the root
                    self.root = None

            # Case 2: Node has only right child
            elif not node.left:
                if parent:
                    if parent.left == node:
                        parent.left = node.right
                    else:
                        parent.right = node.right
                else:  # Deleting the root
                    self.root = node.right

            # Case 3: Node has only left child
            elif not node.right:
                if parent:
                    if parent.left == node:
                        parent.left = node.left
                    else:
                        parent.right = node.left
                else:  # Deleting the root
                    self.root = node.left

            # Case 4: Node has two children
            else:
                # Find the in-order successor (smallest value in right subtree)
                successor = self._find_min(node.right)
                node.data = successor.data  # Copy successor data to this node

                # Delete the successor
                self._delete_recursive(node.right, node, successor.data)

            self.size -= 1
            return True

    def _find_min(self, node):
        """Find the node with the minimum value in a subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, data):
        """Search for a node with the given value."""
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        """Helper method to recursively search for a value."""
        if not node:
            return False

        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def _update_height(self):
        """Update the height of the tree."""
        if not self.root:
            self.height = 0
            return

        self.height = self._height(self.root)

    def _height(self, node):
        """Calculate the height of a subtree."""
        if not node:
            return 0

        left_height = self._height(node.left)
        right_height = self._height(node.right)

        return max(left_height, right_height) + 1

    def get_nodes_by_level(self):
        """Return a dictionary of nodes by level for visualization."""
        if not self.root:
            return {}

        result = {}
        self._get_nodes_by_level(self.root, 0, result)
        return result

    def _get_nodes_by_level(self, node, level, result):
        """Helper method to collect nodes by level."""
        if not node:
            return

        if level not in result:
            result[level] = []

        result[level].append(node)

        self._get_nodes_by_level(node.left, level + 1, result)
        self._get_nodes_by_level(node.right, level + 1, result)

