# Python program to display the Fibonacci sequence

def fib(n):
    "recursive"
    if n < 0: raise Exception('Error. N must be >= 0')
    if n <= 1:
        return n
    else:
        return(fib(n-1) + fib(n-2))

def fib2(n):
    if n < 0: raise Exception('Error. N must be >= 0')
    if n <= 1:
        return n
    n_list = [0, 1]
    count = 2
    while count < n:
        n_add = n_list[-1] + n_list[-2]
        n_list.append(n_add)
        count += 1
    for i in n_list:
        print(i)

n = 10

print(fib2(n) )
#for i in range(n):
#    print(fib(i))