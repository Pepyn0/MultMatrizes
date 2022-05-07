""" Matrix """


class Matrix(object):
    """ Matrix """

    def __init__(self, matrix) -> None:
        self._matrix = matrix
        self._row = len(matrix)
        self._column = len(matrix[0])

    @property
    def row(self):
        """ Row """
        return self._row

    @property
    def column(self):
        """ Row """
        return self._column

    def get_row(self, num: int):
        """ get_row """
        return [i for i in self._matrix[num]]

    def get_column(self, num: int):
        """ get_column """
        return [i[num] for i in self._matrix]

    def __str__(self):
        return f'{self._matrix}'

    def __mul__(self, matrix2):
        matrix_result = []

        if matrix2.row == self._column:
            for i in range(self.row):
                matrix_result.append([])

                for j in range(matrix2.column):
                    list_mult = [x * y for x,
                                 y in zip(self.get_row(i), matrix2.get_column(j))]

                    matrix_result[i].append(sum(list_mult))
        return Matrix(matrix_result)


if __name__ == "__main__":

    matriz1 = Matrix([[1, 2], [3, 4], [5, 6]])
    matriz2 = Matrix([[1, 2, 3], [4, 5, 6]])

    print(matriz1 * matriz2)
