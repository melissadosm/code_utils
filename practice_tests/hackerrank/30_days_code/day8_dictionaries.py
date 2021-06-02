
if __name__ == '__main__':
    n = int(input())
    if 1 <= n <= 10e5: pass
    else: raise Exception ('Error in n')

    name_numbers = [input().split() for _ in range(n)]
    phones = {k: v for k,v in name_numbers}

    while True:
        name = input()
        if name:
            if name in phones:
                print('%s=%s' % (name, phones[name]))
            else:
                print('Not found')
        else:
            break
    