while True:
    try:
        N=int(input('Enter a positive number:'))

    except:
        N=-2
    if N>0:
        break
    else:
        print('You need to enter a positive integer')
print('m','m+1','m**(m+1)')
for m in range(1,N+1):
    print(m,m+1,m**(m+1))
