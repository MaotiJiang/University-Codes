from math import sin
from math import cos
from math import tan

while True:
    f=input('Enter a trigonometric function(sin,cos ,tan):')
    if f!='sin'and f != 'cos' and f != 'tan':
        print('Invalid input')
    else:break

while True:
    try:
        a=float(input('Enter the lower bound a:'))
    except:
        a=None
    if a is None:
        print('Invalid input')
    else:
        break

while True:
    try:
        b=float(input('Enter the upper bound b:'))
    except:
        b=None
    if b is None or b<=a:
        print('Invalid input')
    else:
        break

while True:
    try:
        n=int(input('Enter the number of sub-intervals n:'))
    except:
        print('Invalid Number')
    if n<=0:
        print('Invalid Number')
    else:
        break

i=1
result=0
while i<=n:
    result=result+(b - a) / n * eval(f + '(' + str(a + (b - a) / n * (i - 1 / 2)) + ')')
    i=i+1
print(result)
    
