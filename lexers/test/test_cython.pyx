; Cython test file for lexer testing.
; This file contains Cython constructs to test syntax highlighting.

cimport cython
from libc.math cimport sin, cos

cdef int add(int a, int b):
    return a + b

cdef double fibonacci(int n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@cython.boundscheck(False)
@cython.wraparound(False)
def process_list(list values):
    cdef int i
    cdef int n = len(values)
    cdef list result = []
    for i in range(n):
        result.append(values[i] * 2)
    return result

cdef struct Point:
    double x
    double y

cdef class Person:
    cdef public str name
    cdef public int age
    
    def __init__(self, str name, int age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, {self.name}!"
    
    cpdef str greet_c(self):
        return f"Hello, {self.name}!"

def main():
    x = 5
    y = 10
    print(f"Sum: {x + y}")
    
    cdef int counter = 0
    for i in range(10):
        counter += i
    
    cdef list nums = [1, 2, 3, 4, 5]
    print(nums)
    
    p = Person("John", 30)
    print(p.greet())
    
    print("Program completed!")
