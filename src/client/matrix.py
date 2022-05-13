""" Matrix """
import json


def _treatment(message: str):
    """ _treatment """
    matrix_str = json.loads(message)
    matrix_int = []
    for row in matrix_str:
        matrix_int.append(list(map(int, row)))
    return matrix_int


def treatment(message: bytes) -> tuple[list, list]:
    """ treatment -> Trata a mensagem em bytes e
    a tranforma em uma tupla contendo as duas matrizes

    Exemplo:
    ```py
    message = b'[[1,2],[3,4]]*[[5,6],[7,8]]'
    result = treatment(message)
    print(result)
    ([[1,2],[3,4]],[[5,6],[7,8]])
    ```
    """

    input_str = message.decode()
    matrix_str1, matrix_str2 = input_str.split('*')

    matrix_str1 = _treatment(matrix_str1)
    matrix_str2 = _treatment(matrix_str2)
    return (matrix_str1, matrix_str2)


class Matrix(object):
    """ Matrix -> Guarda a matriz com capacidedade de
    implementar alguns calculos"""

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
        """ get_row -> retorna uma linha especifica da matriz """
        return [i for i in self._matrix[num]]

    def get_column(self, num: int):
        """ get_column -> retorna uma coluna especifica da matriz """
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
    message = f'{[[1, 2],[3, 4],[5, 6]]}*{[[1, 2],[3, 4],[5, 6]]}'
    message = message.encode()
    message = treatment(message)
    print(message)

    # matriz1 = Matrix([[1, 2], [3, 4], [5, 6]])
    # matriz2 = Matrix([[1, 2, 3], [4, 5, 6]])

    # print(matriz1 * matriz2)
