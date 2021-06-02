def factorial(n):
    if n <= 1:
        return 1
    else:
        result = n * factorial(n - 1)
        return result

if __name__ == '__main__':
    n = int(input())
    print (factorial(n))