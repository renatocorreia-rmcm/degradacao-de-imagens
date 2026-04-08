import numpy as np
from Fl import Fl


# todo: implement QR decomposition


def to_fl_matrix(M: np.ndarray) -> np.ndarray:
    return np.vectorize(Fl)(M)


def gauss_elimination(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"Matrix is not square: {A.shape}")

    n = len(A)
    aug_matrix = np.c_[A, b]

    for j in range(n):
        # --- PARTIAL PIVOTING ---
        pivot_row = j + np.argmax(np.abs(aug_matrix[j:, j]))

        if abs(aug_matrix[pivot_row, j]) < 1e-15:
            raise ValueError(f"Matrix is singular or nearly singular at column {j}")

        # Swap rows in the augmented matrix
        if pivot_row != j:
            aug_matrix[[j, pivot_row]] = aug_matrix[[pivot_row, j]]
        # --------------------------------------------

        for i in range(j + 1, n):
            k = aug_matrix[i, j] / aug_matrix[j, j]

            for col in range(j, n + 1):
                aug_matrix[i, col] = aug_matrix[i, col] - (k * aug_matrix[j, col])

    s = np.empty(n, dtype=object)

    for i in range(n - 1, -1, -1):
        soma = aug_matrix[i, n]
        for j in range(i + 1, n):
            soma -= aug_matrix[i, j] * s[j]

        s[i] = soma / aug_matrix[i, i]

    return s

# A = np.array([
#     [20, 1, -1],
#     [-3, 33, 2],
#     [-2, 1, 11]
# ])
# b = np.array([8, -11, -3])
#
# A = to_fl_matrix(A)
# b = to_fl_matrix(b)
# print(gauss_elimination(A, b))
# [0.406, -0.286, -0.173]



def LU_factorization(matrix:np.ndarray, fl=False, pivoting=True) -> tuple[np.array]:
    size = matrix.shape[0]

    convert = to_fl_matrix if fl else lambda x: x.astype(np.float64)

    lower = convert(np.eye(size))
    upper = convert(matrix.copy())
    permutation = convert(np.eye(size))

    for i in range(size):
        if pivoting:
            row = i
            pivo = abs(upper[i][i])

            for k in range(i, size):
                if abs(upper[k][i]) > pivo:
                    pivo = abs(upper[k][i])
                    row = k

            if row != i:
                upper[[row, i]] = upper[[i, row]]
                permutation[[row, i]] = permutation[[i, row]]

                for j in range(i):
                    lower[row][j], lower[i][j] = lower[i][j], lower[row][j]

        pivo = upper[i][i]

        if pivo == 0:
            raise Exception("Impossible to LU decompose the given matrix")

        for j in range(i+1, size):
            ml = upper[j][i] / pivo

            lower[j][i] = ml
            upper[j] -= upper[i] * ml

    return permutation, lower, upper

# PA = UL -> A = P⁻¹·UL -> A⁻¹ = (P⁻¹·UL)⁻¹ = L⁻¹U⁻¹·P 
def inverse_matrix(matrix:np.ndarray, fl=False) -> np.ndarray:
    # Ly = B
    # Ux = y
    size = np.shape(matrix)[0]

    inverse = np.zeros((size, size))
    if fl: inverse = to_fl_matrix(inverse)
    
    try:
        permutation, lower, upper = LU_factorization(matrix, fl=fl, pivoting=True)
    except Exception:
        raise Exception("Not inversible")

    for i in range(size):
        b = np.zeros(size)
        b[i] = 1

        # Ly = b
        y = np.zeros(size)
        if fl: y = to_fl_matrix(y)
        for m in range(size):
            y[m] = (b[m] - sum([lower[m][n]*y[n] for n in range(m)])) / lower[m][m]

        # Ux = y
        x = np.zeros(size)
        if fl: x = to_fl_matrix(x)
        for m in range(size-1, -1, -1):
            x[m] = (y[m] - sum([upper[m][n]*x[n] for n in range (m+1, size)])) / upper[m][m]

        for j in range(size):
            inverse[j][i] = x[j]
    
    return inverse @ permutation