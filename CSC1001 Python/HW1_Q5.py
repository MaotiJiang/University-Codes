while True:
    try:
        N=int(input('Enter an positive integer:'))
    except:
       N=-2
    if N<=2:
        print('Invalid Number')
    else:
        break
primeNumber=''
Goal=True
c=0
print('The prime numbers smaller than',N,'include:')
for m in range(2,N):
    for i in range(2,m):
        if m%i==0:
            Goal=False
            break
    if Goal:
        primeNumber=m
        c=c+1
        print(primeNumber,end = '\t')
        if c%8==0:
         print('')
    Goal = True
    
    

