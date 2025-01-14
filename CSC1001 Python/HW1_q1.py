while True:
    try:
        finalAccountValue=float(input('Enter the final account value:'))
    except:
        finalAccountValue=-2
    if finalAccountValue>0:
        break
    else:
        print('Invalid Number')
while True:
    try:
        annualInterestRate=float(input('Enter the annual interest rate:'))
    except:
        annualInterestRate=-2
    if annualInterestRate>0:
        break
    else:
        print('Invalid Number')
e=annualInterestRate/100
while True:
    try:
        theNumberofYears=int(input('Enter the number of years:'))
    except:
        theNumberofYears=-2
    if theNumberofYears>=1:
        break
    else:
        print('Invalid Number')
initialDepositAmount=finalAccountValue/((1+float(e))**theNumberofYears)
print('The initial value is:',initialDepositAmount)
