import numpy as np
from pandas import DataFrame as pdData
import math

SIZE_MATRIX_X = 3
SIZE_MATRIX_Y = 2

def generate_tabinitial(A, b, c):
    [m, n] = A.shape
    if m != b.size:
        print('La taille du \'b\' doit etre egal a la ligne de \'A\' .')
        exit(1)
    if n != c.size:
        print('La taille du \'c\' doit etre egal a la colonne de \'A\'.')
        exit(1)
    
    result = np.column_stack((A, b))
    result = np.append(result, np.column_stack((c, 0)), axis=0)
    return range(n, n + m), result

def generate_tabinitial_withID(A, b, c):
    m, n                = A.shape
    rng, tabinitial     = generate_tabinitial(A, b, c)
    identity            = np.vstack((np.identity(m), np.zeros(m)))
    return rng, np.concatenate((tabinitial, identity), axis=1)

def positive(v):
    return all(v >= 0), np.amin(v), np.where(v == np.amin(v))


def init(tab, A):
    m, n    = A.shape

    opt         = -tab[m, n]
    tab_b       = tab[:m, n]
    tab_c       = np.concatenate((tab[m , 0:n]
         ,tab[m , n + 1:]))

    tab_A       = np.hstack((tab[0:m ,0:n ]
        ,tab[ 0:m , n + 1 :]))

    return opt, tab_b, tab_c, tab_A

def index_smallest_pos(v):
    return np.where(v > 0, v, np.inf).argmin()

def rapportmin(a, b, m):
    out = []
    for i in range(0, m-1):
        if b[i] != 0:
            out.append(a[i] / b[i])
            
    return index_smallest_pos(np.array(out))

# Both of the function below generates a RunTimeWarning: Divide by 0

# def rapportmin_I(a, b, m):
#     out = np.fromiter(
#         map(lambda i:a[i]/b[i] , range(0, m-1))
#         , dtype=np.float)

#     return index_smallest_pos(out)

# def rapportmin_II(a, b):
#     out = np.divide(np.squeeze(a), b[np.newaxis])
#     return index_smallest_pos(out)

def resolution(tab, A, c):
    opt, tab_b, tab_c, tab_A    = init(tab, A)
    m, n                        = tab.shape
    sign, minimum, index_min    = positive(tab_c)
    
    if (index_min[0] > c.size).all():
        index_min = list(index_min)
        index_min[0] += 1
        index_min = tuple(index_min)
    
    tab = tab.astype(np.float32)

    if sign:
        return tab_b, opt
    else:
        if all(tab[:,index_min] <= 0):
            print("La fonction objective n'est pas bornee.")
            exit(1)
        else:
            A_s                 = tab[:A.shape[0],index_min]

            index_pivot         = rapportmin(tab_b, A_s, m)

            ligne_pivot         = tab[index_pivot]
            colonne_pivot       = tab[:,index_min]

            pivot               = tab[index_pivot,index_min]
            
            tab[index_pivot]    = ligne_pivot / float(pivot)
            
            for i in range(0, len(tab)):
                if not np.array_equal(tab[i], tab[index_pivot]):
                    tab[i] = tab[i] - tab[index_pivot] * tab[i, index_min]

            print("\n",pdData(tab))

            return resolution(tab, A, c)


if __name__ == '__main__':

    c = [[1, -7, -4]]
    
    A = [
                [0, 2, 1],
                [0, 1, 1],
                [0, 1, 0]
        ]
    b = [20, 18, 8]

    (c, A, b)   = map(lambda t: np.array(t), [c, A, b])
    
    # Generates random problems to test the code 

    # A = np.random.randint(-25, 25,size = (SIZE_MATRIX_X, SIZE_MATRIX_Y))
    # b = np.random.randint(-25, 25,size = SIZE_MATRIX_X)
    # c = np.random.randint(-25, 25,size = (1, SIZE_MATRIX_Y))

    range_tab1, tab_initail1    = generate_tabinitial_withID(A, b, c)

    data_frame1                 = pdData(tab_initail1)

    print("\tLe tableau initiale est:")
    print(data_frame1)

    x, y                        = resolution(tab_initail1, A, c)
    
    print('\nSolution Optimale:\t', y)
    print('X:\t', x,)
