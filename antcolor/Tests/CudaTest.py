import numpy as np
from timeit import default_timer as timer
from numba import vectorize, float32

@vectorize(["float32(float32,float32)"], target = 'cuda')
def VectorAdd(a,b):
    return a + b
    # for i in range(a.size):
    #         c[i] = a[i] + b[i]

# def main():
print(tuple.__itemsize__)
N = 32000000
A = np.ones(N, dtype=np.float32)
B = np.ones(N, dtype=np.float32)
C = np.zeros(N, dtype=np.float32)

start = timer()
C = VectorAdd(A,B)
vectoradd_time = timer() - start

print(str(vectoradd_time))

