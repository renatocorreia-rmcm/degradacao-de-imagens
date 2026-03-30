import numpy as np
from Fl import Fl
import scipy.linalg as la

def to_fl_matrix(M: np.ndarray) -> np.ndarray:
    return np.vectorize(Fl)(M)

def matrix_mult(M1: np.ndarray, M2: np.ndarray) -> np.ndarray:
    M1_Fl = to_fl_matrix(M1)
    M2_Fl = to_fl_matrix(M2)

    return M1_Fl @ M2_Fl


def LU_fatoration(matrix:np.ndarray, fl=False)->tuple[np.ndarray] | None:
    size = np.shape(matrix)[0]

    lower = np.eye(size ,dtype=np.float64)
    upper = matrix.astype(np.float64)
    #upper = upper.astype(np.float64)

    #lower = to_fl_matrix(lower)
    #upper = to_fl_matrix(upper)

    for i in range(size):
        pivo = upper[i][i]

        # TODO: create partial pivoting
        if pivo == 0: 
            print(f"need partial pivoting")
            return

        for j in range(i+1, size):
            ml = upper[j][i] / pivo

            lower[j][i] = ml
            upper[j] -= (upper[i]*ml)

    return lower, upper

def inverse_matrix(matrix:np.ndarray)->np.ndarray | None:
    # Ly = B
    # Ux = y
    size = np.shape(matrix)[0]

    inverse = np.zeros((size, size))
    inverse = to_fl_matrix(inverse)
    
    lu = LU_fatoration(matrix)

    if lu == None:
        print("não é inversível")
        return

    lower, upper = lu

    for i in range(size):
        b = np.zeros(size)
        b[i] = 1
        
        # Ly = b
        y = np.zeros(size)
        y = to_fl_matrix(y)
        for m in range(size):
            y[m] = (b[m] - sum([lower[m][n]*y[n] for n in range(m)])) / lower[m][m]

        # Ux = y
        x = np.zeros(size)
        x = to_fl_matrix(x)
        for m in range(size-1, -1, -1):
            x[m] = (y[m] - sum([upper[m][n]*x[n] for n in range (m+1, size)])) / upper[m][m]

        for j in range(size):
            inverse[j][i] = x[j]
    
    return inverse


# M1 = np.array([(1,1,1),
#                (2,2,2),
#                (3,3,3)])
# M2 = np.array([(1,1,1),
#                (2,2,2),
#                (3,3,3)])
# 
# print(matrix_mult(M1,M2))

# a = np.array([[3,2,4],[1,1,2],[4,3,-2]])
# 
# a = to_fl_matrix(a)
# 
# l, u = LU_fatoration(a)
# print(l,"\n")
# print(u,"\n")

# print(inverse_matrix(np.array([[3,2,4],[1,1,2],[4,3,-2]])))