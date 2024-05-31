class Node:
    __slots__ = "row", "col", "data", "next"

    def __init__(self, row=0, col=0, data=0, next_node=None):
        self.row = row
        self.col = col
        self.data = data
        self.next = next_node

class SparseMatrix:
    def __init__(self, num_rows=None, num_cols=None, matrix_file_path=None):
        self.head = None
        self.tail = None
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.size = 0
        if matrix_file_path:
            self.load_matrix(matrix_file_path)

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def _create_node(self, row, col, data):
        new_node = Node(row, col, data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def load_matrix(self, matrix_file_path):
        try:
            with open(matrix_file_path, 'r') as file:
                lines = file.readlines()
                self.num_rows = int(lines[0].split('=')[1].strip())
                self.num_cols = int(lines[1].split('=')[1].strip())
                self.head = self.tail = None
                self.size = 0
                for line in lines[2:]:
                    line = line.strip()
                    if line:
                        if line.startswith('(') and line.endswith(')'):
                            row, col, value = map(int, line[1:-1].split(','))
                            if value != 0:
                                self._create_node(row, col, value)
                        else:
                            raise ValueError("Invalid format in input file")
        except Exception as e:
            raise ValueError("Invalid format in input file") from e

    def get_element(self, row, col):
        current = self.head
        while current:
            if current.row == row and current.col == col:
                return current.data
            current = current.next
        return 0

    def set_element(self, row, col, value):
        current = self.head
        prev = None
        while current:
            if current.row == row and current.col == col:
                if value == 0:
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = prev
                    self.size -= 1
                else:
                    current.data = value
                return
            prev = current
            current = current.next
        if value != 0:
            self._create_node(row, col, value)

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = SparseMatrix(self.num_rows, self.num_cols)
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.data)
            current = current.next
        current = other.head
        while current:
            result.set_element(current.row, current.col, result.get_element(current.row, current.col) + current.data)
            current = current.next
        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")

        result = SparseMatrix(self.num_rows, self.num_cols)
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.data)
            current = current.next
        current = other.head
        while current:
            result.set_element(current.row, current.col, result.get_element(current.row, current.col) - current.data)
            current = current.next
        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Invalid dimensions for multiplication")

        result = SparseMatrix(self.num_rows, other.num_cols)
        current_a = self.head
        while current_a:
            current_b = other.head
            while current_b:
                if current_a.col == current_b.row:
                    result.set_element(current_a.row, current_b.col, result.get_element(current_a.row, current_b.col) + current_a.data * current_b.data)
                current_b = current_b.next
            current_a = current_a.next
        return result

    def print_matrix(self):
        current = self.head
        while current:
            print(f"({current.row}, {current.col}, {current.data})")
            current = current.next

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python sparse_matrix.py <matrix1> <matrix2> <operation>")
        return

    matrix1_path = sys.argv[1]
    matrix2_path = sys.argv[2]
    operation = sys.argv[3]

    try:
        matrix1 = SparseMatrix(matrix_file_path=matrix1_path)
        matrix2 = SparseMatrix(matrix_file_path=matrix2_path)

        if operation == 'add':
            result = matrix1.add(matrix2)
        elif operation == 'subtract':
            result = matrix1.subtract(matrix2)
        elif operation == 'multiply':
            result = matrix1.multiply(matrix2)
        else:
            print("Invalid operation. Choose from 'add', 'subtract', 'multiply'.")
            return

        result.print_matrix()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
