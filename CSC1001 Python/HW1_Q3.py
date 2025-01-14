while True:
    try:
        m=int(input('Enter a positive number:'))
    except:
        m=-2
    if m>0:
        break
    else:
        print('Invalid Number')
n=1
while True:
    if n**2>m:
        break
    n=n+1
print('The smallest integer n is:',n)
    
