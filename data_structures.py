class Array:
    """A simple dynamic array implementation with manual resizing, insertion, deletion, and access."""

    def __init__(self, capacity=16):
        # Underlying storage initialized to fixed capacity
        self._data = [None] * capacity
        self._size = 0  # Number of actual elements stored

    def __len__(self):
        """Return number of elements currently in the array."""
        return self._size

    def insert(self, index, value):
        """
        Insert value at the given index.
        Shifts elements to the right as needed. Resizes (doubling) if storage is full.
        Amortized O(1) for append, O(n) for arbitrary position due to shifting.
        """
        if index < 0 or index > self._size:
            raise IndexError('Index out of bounds')
        # Resize to accommodate new element if full
        if self._size == len(self._data):
            self._resize(len(self._data) * 2)
        # Shift elements rightward to make room
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index):
        """
        Delete and return element at index.
        Shifts elements leftward to fill gap. Shrinks storage (halving) if too sparse.
        """
        if index < 0 or index >= self._size:
            raise IndexError('Index out of bounds')
        val = self._data[index]
        # Shift elements to cover the deleted slot
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        # Clear duplicate at end and decrement size
        self._data[self._size - 1] = None
        self._size -= 1
        # Shrink underlying storage to avoid wasted space (when quarter full)
        if 0 < self._size <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        return val

    def access(self, index):
        """Return element at index without modification."""
        if index < 0 or index >= self._size:
            raise IndexError('Index out of bounds')
        return self._data[index]

    def _resize(self, new_cap):
        """Internal: resize underlying storage to new capacity, copying existing elements."""
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data


class Stack:
    """Simple stack (LIFO) built on top of Python list."""

    def __init__(self):
        self._arr = []

    def push(self, x):
        """Push element onto stack. O(1)."""
        self._arr.append(x)

    def pop(self):
        """Pop and return top element. Raises if empty. O(1)."""
        if not self._arr:
            raise IndexError('Pop from empty stack')
        return self._arr.pop()

    def peek(self):
        """Return top element without removing it. O(1)."""
        if not self._arr:
            raise IndexError('Peek from empty stack')
        return self._arr[-1]

    def is_empty(self):
        """Check if stack is empty."""
        return len(self._arr) == 0

    def size(self):
        """Return number of elements in stack."""
        return len(self._arr)


class Queue:
    """Amortized O(1) queue using list with lazy head pointer to avoid shifting per dequeue."""

    def __init__(self):
        self._arr = []
        self._head = 0  # Index of current front element

    def enqueue(self, x):
        """Add element to back of queue. O(1)."""
        self._arr.append(x)

    def dequeue(self):
        """
        Remove and return front element.
        Uses lazy deletion: advances head pointer and periodically compacts internal list to prevent unbounded growth.
        Amortized O(1).
        """
        if self._head >= len(self._arr):
            raise IndexError('Dequeue from empty queue')
        val = self._arr[self._head]
        self._head += 1
        # Cleanup when head has consumed more than half to reclaim space
        if self._head > len(self._arr) // 2:
            self._arr = self._arr[self._head:]
            self._head = 0
        return val

    def peek(self):
        """Return front element without removing it."""
        if self._head >= len(self._arr):
            raise IndexError('Peek from empty queue')
        return self._arr[self._head]

    def is_empty(self):
        """Check if queue has no elements."""
        return self._head >= len(self._arr)

    def size(self):
        """Return number of elements currently in queue."""
        return len(self._arr) - self._head
